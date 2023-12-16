from xgboost import XGBClassifier

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, auc
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import os
from datetime import datetime, timedelta
import time

from kaggle.api.kaggle_api_extended import KaggleApi

import joblib

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

# Function to train an XGBoost model
def train_xgboost_model(X_train, y_train):
    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb_model.fit(X_train, y_train)
    return xgb_model

# Function to evaluate the trained model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    precision, recall, _ = precision_recall_curve(y_test, model.predict_proba(X_test)[:, 1])
    auc_pr = auc(recall, precision)
    return y_pred, auc_pr

# Function to create a confusion matrix
def create_confusion_matrix(y_test, y_pred):
    return confusion_matrix(y_test, y_pred)

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