import time
import yaml
from influxdb import InfluxDBClient

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

def write_performance_test(num_records):
    """Test write performance by inserting num_records into the InfluxDB measurement."""
    start_time = time.time()
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
    end_time = time.time()
    duration = end_time - start_time
    print(f"Write Performance Test: Inserted {num_records} records in {duration:.2f} seconds")

def read_performance_test(num_records):
    """Test read performance by querying the last num_records from the InfluxDB measurement."""
    query = f"SELECT * FROM {INFLUXDB_MEASUREMENT} ORDER BY time DESC LIMIT {num_records}"
    start_time = time.time()
    results = client.query(query)
    points = list(results.get_points())
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
