This Porject is an end-to-end data processing project using Apache Kafka and Apache Airflow. The project involves taking data from a Kafka stream, batch processing it with Airflow

Key steps and components:

Kafka Producer: A simple Python script simulates data generation and sends it to a Kafka topic.
Airflow DAG:
Kafka Message Collection Task: Collects 100 messages from the Kafka topic and saves them as a CSV file.
Data Cleaning Task: Reads the CSV file, cleans the data (e.g., dropping null values, converting to uppercase), and saves it as a new CSV file.


Data is generated and sent to a Kafka topic.
Airflow's scheduler triggers the Kafka message collection task.
The task collects 100 messages and saves them as a CSV file.
Airflow triggers the data cleaning task.
The task cleans the data and saves it as a new CSV file.
Airflow triggers the Spark ML job task.
