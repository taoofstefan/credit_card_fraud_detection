# Credit Card Fraud Detection Application using Docker

This project is a comprehensive machine learning system designed to detect fraudulent transactions in credit card data. The system is built on a microservices architecture, with each component containerized using Docker, ensuring isolation, scalability, and ease of deployment. The architecture is optimized for high-volume data streaming, capable of processing and analyzing data in real-time.

## Machine Learning Approach

The core of the system is the machine learning model, an XGBoost classifier, trained to identify patterns indicative of fraud. The model is trained on a preprocessed dataset where features have been standardized and class imbalances addressed using SMOTE (Synthetic Minority Over-sampling Technique). This preprocessing step is crucial for the model’s performance, as it ensures that the minority class (fraudulent transactions) is adequately represented.

Once trained, the model’s performance is evaluated using a variety of metrics, including precision, recall, and F1 score, to ensure its effectiveness in detecting fraudulent transactions. A confusion matrix is also generated and visualized to provide insights into the model’s prediction capabilities.

<p align="center">
  <img src="https://github.com/taoofstefan/credit_card_fraud_detection/blob/main/documentation/confusion_matrix.png" width="500" height=auto alt="Confusion Matrix">
</p>

## Data Flow and Machine Learning Process
The data flow in your system begins with the Kaggle API, which is used to download the credit card transaction dataset. This dataset is then preprocessed and balanced using SMOTE within the train_model microservice. The preprocessed data is split into training and testing sets, and an XGBoost classifier is trained on the training set. The trained model is then evaluated on the testing set, and the results are visualized in a confusion matrix. The trained model is saved as a .pkl file for later use.

Once the model is trained and saved, the producer microservice comes into play. It simulates real-time transaction data by applying small random perturbations to the features of the preprocessed dataset. This simulates the natural variability that would be expected in real-world transaction data. The perturbed data is then sent to a Kafka topic as a stream of messages.

The consumer microservice subscribes to this Kafka topic and consumes the streaming data. It loads the previously trained XGBoost model and uses it to make predictions on the incoming data. If a transaction is predicted as potentially fraudulent, it is stored in an SQLite database.

## Containerization and Data Streaming
Each component of the system is encapsulated within a Docker container, which includes the necessary dependencies and runtime environment. This containerization approach allows for easy replication of the system across different environments and simplifies the management of dependencies.

The system utilizes Apache Kafka for data streaming, with a producer service that simulates real-time transaction data and publishes it to a Kafka topic. Kafka’s distributed nature and high throughput make it an ideal choice for handling the volume and velocity of data typical in financial transaction systems.

The consumer service subscribes to the Kafka topic, ingests the streaming data, and uses the trained XGBoost model to make predictions on each transaction. Transactions predicted as potentially fraudulent are stored in an SQLite database, which serves as a persistent storage solution for further analysis or investigation.

## High Volume Data Handling
To accommodate high volumes of data, the system is designed with scalability in mind. Kafka’s ability to handle large data streams, combined with the horizontal scalability of Docker containers, allows the system to scale up or down based on the incoming data load. This ensures that the system remains responsive and efficient, even under heavy data traffic.

## Project Flowchart
![Credit Card Fraud Detection Backend](https://github.com/taoofstefan/credit_card_fraud_detection/blob/main/documentation/credit%20card%20fraud%20kaggle%20back%20end.png)

## Requirements
To run this project you need to install Docker on your system.

### Optional
Install Coding IDE like VS Code that connects to you Docker installation. It makes running things smoother.

## API Reference

#### Kaggle API


| Parameter | Type     | Description   |
| :-------- | :------- | :------------ |
| `username` | `string` | **Required** |
| `key`      | `string` | **Required** |

#### To connect to Kaggle a api_key is required. Loging to your kaggle account on kaggle.com -> go to Settings and create a new tokken. This will let you download a kaggle.json file with a username and a key.
This key needs to be stored in the /shared folder of the project to make the neccessary api calls.



## Run Locally

Clone the project

```bash
  git clone [https://link-to-project](https://github.com/taoofstefan/credit_card_fraud_detection.git)
```

Go to the project directory

```bash
  cd my-project
```

Start the project using Docker

```bash
  docker-compose up --build
```
