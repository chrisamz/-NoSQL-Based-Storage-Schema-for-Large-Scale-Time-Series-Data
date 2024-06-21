from influxdb import InfluxDBClient

# Load configuration
import yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# InfluxDB configuration
INFLUXDB_HOST = config['influxdb']['host']
INFLUXDB_PORT = config['influxdb']['port']
INFLUXDB_DATABASE = config['influxdb']['database']
INFLUXDB_MEASUREMENT = config['influxdb']['measurement']

# Connect to InfluxDB
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)

# Create Database
client.create_database(INFLUXDB_DATABASE)

# Switch to the created database
client.switch_database(INFLUXDB_DATABASE)

# Sample data to insert
data = [
    {
        "measurement": INFLUXDB_MEASUREMENT,
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2024-06-01T00:00:00Z",
        "fields": {
            "value": 0.64
        }
    },
    {
        "measurement": INFLUXDB_MEASUREMENT,
        "tags": {
            "host": "server02",
            "region": "us-west"
        },
        "time": "2024-06-01T00:01:00Z",
        "fields": {
            "value": 0.65
        }
    }
]

# Write data to InfluxDB
client.write_points(data)

print(f"Database '{INFLUXDB_DATABASE}' and measurement '{INFLUXDB_MEASUREMENT}' setup complete with sample data inserted.")
