import time
import yaml
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

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

def write_performance_test(num_records):
    """Test write performance by inserting num_records into the Cassandra table."""
    start_time = time.time()
    for i in range(num_records):
        timestamp = int(time.time() * 1000)
        value = i
        query = f"INSERT INTO {CASSANDRA_TABLE} (timestamp, value) VALUES (%s, %s)"
        session.execute(query, (timestamp, value))
    end_time = time.time()
    duration = end_time - start_time
    print(f"Write Performance Test: Inserted {num_records} records in {duration:.2f} seconds")

def read_performance_test(num_records):
    """Test read performance by querying the last num_records from the Cassandra table."""
    query = f"SELECT * FROM {CASSANDRA_TABLE} LIMIT %s"
    start_time = time.time()
    rows = session.execute(query, (num_records,))
    end_time = time.time()
    duration = end_time - start_time
    print(f"Read Performance Test: Queried {num_records} records in {duration:.2f} seconds")

def main():
    num_records = 1000  # Adjust the number of records for performance testing

    # Write Performance Test
    write_performance_test(num_records)

    # Read Performance Test
    read_performance_test(num_records)

if __name__ == '__main__':
    main()
