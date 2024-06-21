import random
import time
import json
import yaml
from kafka import KafkaProducer

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

KAFKA_BROKER = config['kafka']['broker']
TOPIC = config['kafka']['topic']
DATA_GENERATION_INTERVAL = config['data_generation']['interval']  # in seconds

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
        time.sleep(DATA_GENERATION_INTERVAL)  # Adjust the interval as per the configuration

if __name__ == '__main__':
    try:
        produce_data()
    except KeyboardInterrupt:
        print('Data generation stopped.')
    finally:
        producer.close()
