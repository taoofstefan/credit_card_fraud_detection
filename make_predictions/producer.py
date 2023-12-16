from functions import *
from kafka import KafkaProducer
import time
import json

if __name__ == "__main__":
    time.sleep(35)  # Adjust the delay as needed

    # Connect to Kaggle
    api = KaggleApi()
    api.authenticate()

    # Define the dataset and download path
    dataset_name = "mlg-ulb/creditcardfraud"
    download_path = "download"

    # Download the dataset
    download_dataset(api, dataset_name, download_path)

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(os.path.join(download_path, [file for file in os.listdir(download_path) if file.endswith('.csv')][0]))

    # Preprocess data
    df = preprocess_data(df)

    # Handle imbalanced data
    X_resampled, y_resampled = handle_imbalanced_data(df.drop("Class", axis=1), df["Class"])

    # Simulate streaming data with small random perturbations
    streaming_data = X_resampled.copy()

    # Perturb the features (excluding 'Time', 'Class', and 'std_Amount')
    perturbation_factor = 0.001  # Adjust as needed
    streaming_data.iloc[:, 1:-3] *= (1 + np.random.uniform(-perturbation_factor, perturbation_factor, size=streaming_data.iloc[:, 1:-3].shape))

    # Kafka Producer
    producer = KafkaProducer(bootstrap_servers='kafka:9092', 
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    print("Producer is starting...")

    while(True):
        # Make a copy to avoid modifying the original DataFrame
        sampled_row = streaming_data.sample(n=1).copy()  

        # Send data to Kafka
        producer.send('my-topic', sampled_row.to_dict())


print("Producer finished sending messages.")
producer.close()
print("Producer closed.")