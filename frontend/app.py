from flask import Flask, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

# Database file path
DATABASE = '/data/fraud_detection.db'

@app.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)
    # Query the database to retrieve data
    query = "SELECT * FROM potential_fraud"
    df = pd.read_sql_query(query, conn)
    # Close the database connection
    conn.close()
    # Render the data in an HTML table
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
