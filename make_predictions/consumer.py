from functions import *
from kafka import KafkaConsumer
import time
import json
import sqlite3

if __name__ == "__main__":
    # Connect to the SQLite database
    conn = sqlite3.connect('fraud_detection.db')
    cursor = conn.cursor()

    # Check if the table exists, and create it if not
    cursor.execute('''CREATE TABLE IF NOT EXISTS potential_fraud (
    Time TEXT,
    V1 REAL, V2 REAL, V3 REAL, V4 REAL, V5 REAL, V6 REAL, V7 REAL, V8 REAL, V9 REAL, V10 REAL,
    V11 REAL, V12 REAL, V13 REAL, V14 REAL, V15 REAL, V16 REAL, V17 REAL, V18 REAL, V19 REAL,
    V20 REAL, V21 REAL, V22 REAL, V23 REAL, V24 REAL, V25 REAL, V26 REAL, V27 REAL, V28 REAL,
    std_Amount REAL);''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    # Load the model from the .pkl file
    loaded_model = joblib.load('/models/xgb_model.pkl')

    # Define the columns for the potential fraud DataFrame
    columns = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9','V10', 
               'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 
               'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28']

    # Create an empty DataFrame for potential fraud
    potential_fraud = pd.DataFrame(columns=columns)

    # Add a delay before creating the KafkaConsumer
    time.sleep(40)  # Adjust the delay as needed

    print("Consumer is starting...")
    # Kafka Consumer
    consumer = KafkaConsumer('my-topic', bootstrap_servers='kafka:9092', 
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    for message in consumer:
        data = message.value    
        X_sample = pd.DataFrame.from_dict(data)

        # Make predictions using the loaded XGBoost model
        prediction = loaded_model.predict(X_sample)    
            
        if prediction[0] == 1: 
            current_time = get_current_time()

            # Use the current time for the 'Time' column
            X_sample['Time'] = current_time 

            # Convert 'Time' column to datetime format
            X_sample['Time'] = pd.to_datetime(X_sample['Time'], format='%Y-%m-%d %H:%M:%S.%f')  

            # Concatenate the row to the potential_fraud DataFrame
            potential_fraud = pd.concat([potential_fraud, X_sample], ignore_index=True) 

            # Convert Timestamp to string
            current_time_str = str(X_sample['Time'].iloc[0])

            # Use the string representation for 'Time' column
            X_sample['Time'] = current_time_str
                       
            print("Potential fraud detected:", current_time)

            # Connect to the SQLite database
            conn = sqlite3.connect('fraud_detection.db')
            cursor = conn.cursor()
            
            # Insert the potential fraud data into the database
            cursor.execute('''
                INSERT INTO potential_fraud VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', tuple(X_sample.iloc[0]))

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

    consumer.close()
    print("Consumer closed.")