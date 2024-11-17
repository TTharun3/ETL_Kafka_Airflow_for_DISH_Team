from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
@dag(default_args=default_args, schedule_interval=timedelta(minutes=5), catchup=False)
def kafka_to_spark_ml():
    @task
    def collect_kafka_messages():
        from kafka import KafkaConsumer
        import pandas as pd
        import json

        # Initialize Kafka consumer
        consumer = KafkaConsumer(
            'my_topic',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        # Collect messages
        messages = []
        for _ in range(100):  # Adjust the number of messages as needed
            msg = next(consumer)
            messages.append(msg.value)
        
        # Convert messages to a Pandas DataFrame
        df = pd.DataFrame(messages)
        
        # Save DataFrame to a CSV file
        file_path = '/tmp/kafka_messages.csv'
        df.to_csv(file_path, index=False)
        
        # Close the consumer
        consumer.close()
        
        return file_path

    # Task execution
    collect_kafka_messages()

# Instantiate the DAG
kafka_to_spark_ml_dag = kafka_to_spark_ml()