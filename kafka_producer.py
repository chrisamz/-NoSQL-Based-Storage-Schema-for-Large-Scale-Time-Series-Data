import json
import time
import random
from kafka import KafkaProducer
import yaml

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

KAFKA_BROKER = config['kafka']['broker']
TOPIC = config['kafka']['topic']

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_data():
    """Generate synthetic time-series data."""
    while True:
        data_point = {
            'timestamp': int(time.time() * 1000),
            'value': random.uniform(20.0, 100.0)
        }
        yield data_point

def produce_data():
    """Send data to Kafka topic."""
    for data in generate_data():
        producer.send(TOPIC, data)
        print(f'Sent data: {data}')
        time.sleep(1)  # Adjust the sleep time as per the data generation rate required

if __name__ == '__main__':
    try:
        produce_data()
    except KeyboardInterrupt:
        print('Data production stopped.')
    finally:
        producer.close()
