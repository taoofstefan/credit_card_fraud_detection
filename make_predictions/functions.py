from xgboost import XGBClassifier

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, auc
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE

import pandas as pd
import numpy as np

import os
from datetime import datetime, timedelta
import time

from kaggle.api.kaggle_api_extended import KaggleApi

import joblib
import sqlite3

from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json

# Function to preprocess the dataset
def preprocess_data(df):
    # Standardize 'Amount' column using StandardScaler
    scaler = preprocessing.StandardScaler()
    df['std_Amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
    df = df.drop("Amount", axis=1)  # Drop the original 'Amount' column
    return df

# Function to handle imbalanced data using SMOTE
def handle_imbalanced_data(X, y):
    smote = SMOTE(sampling_strategy=0.5)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    return X_resampled, y_resampled

# Function to download a dataset from Kaggle
def download_dataset(api, dataset_name, download_path):
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)

# Function to get the current time with nanosecond precision
def get_current_time():
    current_time_ns = time.time_ns()  # Get the current time in nanoseconds
    seconds = current_time_ns // 1_000_000_000
    nanoseconds = current_time_ns % 1_000_000_000
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seconds))
    current_time = f"{formatted_time}.{nanoseconds:09d}"
    return current_time

# Create and return a KafkaConsumer instance.
def create_consumer():
    return KafkaConsumer('my-topic', bootstrap_servers='kafka:9092')

# Consume messages from Kafka topic 'my-topic'.
def consume_messages():
    consumer = None
    max_retries = 6
    retries = 0

    while retries < max_retries:
        try:
            # Attempt to create a KafkaConsumer
            consumer = create_consumer()
            print("Consumer is starting...")
            break  # Exit the loop if consumer is successfully created
        except NoBrokersAvailable:
            # Handle the case when no brokers are available
            retries += 1
            print(f"Retrying in 10 seconds (retry {retries}/{max_retries})...")
            time.sleep(10)
        except Exception as e:
            # Handle other exceptions that may occur during consumer creation
            print(f"An error occurred: {e}")
        finally:
            # Close the consumer if it was created but encountered an issue
            if consumer:
                consumer.close()