-- Create Keyspace
CREATE KEYSPACE IF NOT EXISTS timeseries WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': '1'
};

-- Use Keyspace
USE timeseries;

-- Create Table
CREATE TABLE IF NOT EXISTS data (
  timestamp bigint,
  value double,
  PRIMARY KEY (timestamp)
) WITH CLUSTERING ORDER BY (timestamp ASC);
