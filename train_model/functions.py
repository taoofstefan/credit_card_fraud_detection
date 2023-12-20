import joblib
from xgboost import XGBClassifier

import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns

import os
from datetime import datetime, timedelta
import time

from kaggle.api.kaggle_api_extended import KaggleApi

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, auc
from sklearn.metrics import confusion_matrix

from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import joblib

# Function to preprocess the dataset
def preprocess_data(df):
    # Create a StandardScaler for standardizing the 'Amount' column
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
    # Initialize an XGBoost classifier
    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb_model.fit(X_train, y_train)  # Train the model
    return xgb_model

# Function to evaluate the trained model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)  # Predict on the test set
    precision, recall, _ = precision_recall_curve(y_test, model.predict_proba(X_test)[:, 1])
    auc_pr = auc(recall, precision)  # Calculate AUC-PR
    return y_pred, auc_pr

# Function to create a confusion matrix
def create_confusion_matrix(y_test, y_pred):
    return confusion_matrix(y_test, y_pred)

# Function to download a dataset from Kaggle
def download_dataset(api, dataset_name, download_path):
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)