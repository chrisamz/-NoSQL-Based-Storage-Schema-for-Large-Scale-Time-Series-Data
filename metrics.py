import time
import yaml
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from metrics import measure_time, write_performance, read_performance

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Cassandra configuration
CASSANDRA_CONTACT_POINTS = config['cassandra']['contact_points']
CASSANDRA_KEYSPACE = config['cassandra']['keyspace']
CASSANDRA_TABLE = config['cassandra']['table']

# Connect to Cassandra
cluster = Cluster(CASSANDRA_CONTACT_POINTS)
session = cluster.connect(CASSANDRA_KEYSPACE)

@measure_time
def write_to_cassandra(num_records):
    for i in range(num_records):
        timestamp = int(time.time() * 1000)
        value = i
        query = f"INSERT INTO {CASSANDRA_TABLE} (timestamp, value) VALUES (%s, %s)"
        session.execute(query, (timestamp, value))

@measure_time
def read_from_cassandra(num_records):
    query = f"SELECT * FROM {CASSANDRA_TABLE} LIMIT %s"
    session.execute(query, (num_records,))

def main():
    num_records = 1000  # Adjust the number of records for performance testing

    # Write Performance Test
    write_performance(num_records, write_to_cassandra)

    # Read Performance Test
    read_performance(num_records, read_from_cassandra)

if __name__ == '__main__':
    main()

import time
import yaml
from influxdb import InfluxDBClient
from metrics import measure_time, write_performance, read_performance

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# InfluxDB configuration
INFLUXDB_HOST = config['influxdb']['host']
INFLUXDB_PORT = config['influxdb']['port']
INFLUXDB_DATABASE = config['influxdb']['database']
INFLUXDB_MEASUREMENT = config['influxdb']['measurement']

# Connect to InfluxDB
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
client.switch_database(INFLUXDB_DATABASE)

@measure_time
def write_to_influxdb(num_records):
    points = []
    for i in range(num_records):
        timestamp = int(time.time() * 1000)
        value = i
        point = {
            "measurement": INFLUXDB_MEASUREMENT,
            "time": timestamp,
            "fields": {
                "value": value
            }
        }
        points.append(point)
    client.write_points(points)

@measure_time
def read_from_influxdb(num_records):
    query = f"SELECT * FROM {INFLUXDB_MEASUREMENT} ORDER BY time DESC LIMIT {num_records}"
    client.query(query)

def main():
    num_records = 1000  # Adjust the number of records for performance testing

    # Write Performance Test
    write_performance(num_records, write_to_influxdb)

    # Read Performance Test
    read_performance(num_records, read_from_influxdb)

if __name__ == '__main__':
    main()
