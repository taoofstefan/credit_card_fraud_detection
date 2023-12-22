# Credit Card Fraud Detection Application using Docker

This project is a comprehensive machine learning system designed to detect fraudulent transactions in credit card data. The system is built on a microservices architecture, with each component containerized using Docker, ensuring isolation, scalability, and ease of deployment. The architecture is optimized for high-volume data streaming, capable of processing and analyzing data in real-time.

## Machine Learning Approach

The core of the system is the machine learning model, an XGBoost classifier, trained to identify patterns indicative of fraud. The model is trained on a preprocessed dataset where features have been standardized and class imbalances addressed using SMOTE (Synthetic Minority Over-sampling Technique). This preprocessing step is crucial for the model’s performance, as it ensures that the minority class (fraudulent transactions) is adequately represented.

Once trained, the model’s performance is evaluated using a variety of metrics, including precision, recall, and F1 score, to ensure its effectiveness in detecting fraudulent transactions.

<p align="center">
  <img src="https://github.com/taoofstefan/credit_card_fraud_detection/blob/main/documentation/train_model_scores.png" width="500" height=auto alt="Training Scores">
</p>

A confusion matrix is also generated and visualized to provide insights into the model’s prediction capabilities.

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

## Frontend Architecture and Design Highlights

The frontend of the machine learning system is a sophisticated and user-friendly web interface, designed to visualize and interact with the data processed by the backend services. It serves as a crucial component for monitoring and analyzing the results of the machine learning model's predictions on fraudulent credit card transactions. Developed using modern web technologies, the frontend stands out for its responsiveness, ease of use, and aesthetic appeal.

### Technical Stack and Implementation

Flask Web Framework: The frontend is built using Flask, a lightweight and powerful web framework for Python. Flask's simplicity and flexibility make it an ideal choice for serving dynamic web pages and handling HTTP requests efficiently.

HTML and Bootstrap: The user interface is structured with HTML, styled using Bootstrap, a popular CSS framework. Bootstrap's responsive design ensures that the frontend is accessible and visually appealing across various devices and screen sizes.

Custom CSS: Additional styling is provided through custom CSS rules, further refining the user interface's look and feel. These styles are organized in a separate stylesheet (styles.css), ensuring a clean separation of content and presentation.

### Design Highlights

Interactive Data Table: Central to the frontend is an interactive table displaying the potentially fraudulent transactions. The table is dynamically generated from the SQLite database, where the consumer microservice stores the transactions flagged by the machine learning model.
<p align="center">
  <img src="https://github.com/taoofstefan/credit_card_fraud_detection/blob/main/documentation/frontend_overview.png" alt="Frontend Overview">
</p>


Favicon Integration: A custom favicon is integrated into the web interface, enhancing brand identity and visual recognition in browser tabs.

<p align="center">
  <img src="https://github.com/taoofstefan/credit_card_fraud_detection/blob/main/documentation/frontend_favicon.png" alt="Frontend Favicon">
</p>

Pagination: To efficiently manage and navigate through large volumes of data, the frontend implements pagination. This feature limits the number of entries displayed per page, with navigation controls enabling users to traverse between pages seamlessly.

<p align="center">
  <img src="https://github.com/taoofstefan/credit_card_fraud_detection/blob/main/documentation/frontend_paging.png" alt="Frontend Paging">
</p>

Search Functionality: A key feature of the frontend is a search box that allows users to filter transactions by specific dates or detailed timestamps. This functionality greatly enhances the user experience by providing a quick and intuitive means to access relevant data.

<p align="center">
  <img src="https://github.com/taoofstefan/credit_card_fraud_detection/blob/main/documentation/frontend_search.png" alt="Frontend Search">
</p>

Alternating Row Coloring: For improved readability, the data table implements alternating row coloring. This zebra-striping effect, achieved through CSS, makes it easier for users to differentiate between rows of data, reducing visual fatigue and enhancing data comprehension.

Responsive Design: The frontend's responsive design ensures that it adapts gracefully to different screen sizes and resolutions. This responsiveness is crucial for accessibility, allowing users to interact with the system on various devices, from desktop computers to mobile phones.

### User Experience and Accessibility
The frontend is optimized for performance and efficiency. It features efficient data loading and pagination, significantly reducing the data volume displayed per page, which enhances page load times and user experience for extensive datasets. Static assets like CSS files are cached, minimizing server requests and accelerating load times for recurring visits. The architecture is designed to minimize blocking HTTP requests, contributing to a smooth and responsive user interface. Moreover, the use of Bootstrap for responsive design ensures swift rendering across various devices, further optimizing the frontend's performance.

### Security and Performance
While focused on user experience and functionality, the frontend also adheres to best practices in web security and performance optimization. It employs strict input validation and sanitization to safeguard against SQL injection, especially in search functionalities. Secure HTTP headers, including Content Security Policy and X-Content-Type-Options, are rigorously applied to prevent cross-site scripting and content type sniffing. Additionally, the system leverages Flask’s built-in session management for secure, encrypted session handling, preventing session hijacking and ensuring data is transmitted securely. Error handling is meticulously managed to prevent leakage of sensitive information, with Flask's custom error pages concealing technical error details from end users.

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
  git clone https://github.com/taoofstefan/credit_card_fraud_detection.git
```

Go to the project directory

```bash
  cd credit_card_fraud_detection-main
```

Start the project using Docker

```bash
  docker-compose up --build
```
Open your webbrowser

```bash
  localhost:5000
```