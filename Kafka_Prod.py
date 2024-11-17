import requests
from kafka import KafkaProducer
import json

def fetch_data_from_api(api_url, num_records):
    """
    Fetch random user data from the Random User Generator API.
    """
    users = []
    for _ in range(num_records):
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            # Extract relevant fields from API response
            for result in data.get('results', []):
                user = {
                    "name": f"{result['name']['first']} {result['name']['last']}",
                    "email": result['email'],
                    "location": f"{result['location']['city']}, {result['location']['country']}",
                    "phone": result['phone'],
                    "age": result['dob']['age']
                }
                users.append(user)
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
    return users

def produce_messages_to_kafka(topic, data):
    """
    Produce messages to Kafka from the fetched API data.
    """
    # Set up Kafka producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    # Send each user record as a message to Kafka
    for record in data:
        producer.send(topic, record)
        print(f"Sent to Kafka: {record}")
    
    # Flush and close producer
    producer.flush()
    producer.close()

if __name__ == "__main__":
    # Random User Generator API endpoint
    api_url = "https://randomuser.me/api/"  # This endpoint returns random user data
    
    # Number of records to fetch
    num_records = 100  # Adjust this number as needed
    
    # Fetch data from API
    data = fetch_data_from_api(api_url, num_records)
    
    # Produce messages to Kafka
    produce_messages_to_kafka('my_topic', data)