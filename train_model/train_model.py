import warnings
warnings.filterwarnings('ignore')
from functions import *

if __name__ == "__main__":
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

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

    # Train the XGBoost model
    xgb_model = train_xgboost_model(X_train, y_train)

    # Evaluate the model
    y_pred_xgb, auc_pr = evaluate_model(xgb_model, X_test, y_test)

    # Create a confusion matrix
    conf_mat = confusion_matrix(y_test, y_pred_xgb)

    # Plot the confusion matrix using seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues', xticklabels=['Predicted 0', 'Predicted 1'], yticklabels=['Actual 0', 'Actual 1'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')

    # Save the plot as an image file
    plt.savefig('/app/train_model/confusion_matrix.png')

    # Scores
    print("Scores from the trained model:")
    print("Accuracy XGBoost:", np.mean(y_pred_xgb == y_test))
    print("Precision XGBoost:", np.sum((y_pred_xgb == 1) & (y_test == 1)) / np.sum(y_pred_xgb == 1))
    print("Recall XGBoost:", np.sum((y_pred_xgb == 1) & (y_test == 1)) / np.sum(y_test == 1))
    print("F1 Score XGBoost:", 2 * np.sum((y_pred_xgb == 1) & (y_test == 1)) / (np.sum(y_pred_xgb == 1) + np.sum(y_test == 1)))

    # Save the model to a .pkl file
    joblib.dump(xgb_model, '/models/xgb_model.pkl')
    print("Trained model has been saved")
