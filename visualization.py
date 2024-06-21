import argparse
import yaml
import matplotlib.pyplot as plt
from cassandra.cluster import Cluster
from influxdb import InfluxDBClient

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Cassandra configuration
CASSANDRA_CONTACT_POINTS = config['cassandra']['contact_points']
CASSANDRA_KEYSPACE = config['cassandra']['keyspace']
CASSANDRA_TABLE = config['cassandra']['table']

# InfluxDB configuration
INFLUXDB_HOST = config['influxdb']['host']
INFLUXDB_PORT = config['influxdb']['port']
INFLUXDB_DATABASE = config['influxdb']['database']
INFLUXDB_MEASUREMENT = config['influxdb']['measurement']

# Connect to Cassandra
cassandra_cluster = Cluster(CASSANDRA_CONTACT_POINTS)
cassandra_session = cassandra_cluster.connect(CASSANDRA_KEYSPACE)

# Connect to InfluxDB
influxdb_client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
influxdb_client.switch_database(INFLUXDB_DATABASE)

def query_cassandra(query):
    rows = cassandra_session.execute(query)
    data = [{'timestamp': row.timestamp, 'value': row.value} for row in rows]
    return data

def query_influxdb(query):
    results = influxdb_client.query(query)
    points = results.get_points()
    data = [{'timestamp': point['time'], 'value': point['value']} for point in points]
    return data

def plot_data(data, title):
    timestamps = [d['timestamp'] for d in data]
    values = [d['value'] for d in data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, values, marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title(title)
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Visualization interface for time-series data.')
    parser.add_argument('--db', choices=['cassandra', 'influxdb'], required=True, help='Database to query')
    parser.add_argument('--query', required=True, help='Query to execute')

    args = parser.parse_args()

    if args.db == 'cassandra':
        data = query_cassandra(args.query)
        plot_data(data, 'Cassandra Time-Series Data')
    elif args.db == 'influxdb':
        data = query_influxdb(args.query)
        plot_data(data, 'InfluxDB Time-Series Data')

if __name__ == '__main__':
    main()
