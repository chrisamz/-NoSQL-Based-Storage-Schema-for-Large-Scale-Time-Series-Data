import argparse
import yaml
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
    for row in rows:
        print(row)

def query_influxdb(query):
    results = influxdb_client.query(query)
    points = results.get_points()
    for point in points:
        print(point)

def main():
    parser = argparse.ArgumentParser(description='Query interface for time-series data.')
    parser.add_argument('--db', choices=['cassandra', 'influxdb'], required=True, help='Database to query')
    parser.add_argument('--query', required=True, help='Query to execute')

    args = parser.parse_args()

    if args.db == 'cassandra':
        query_cassandra(args.query)
    elif args.db == 'influxdb':
        query_influxdb(args.query)

if __name__ == '__main__':
    main()
