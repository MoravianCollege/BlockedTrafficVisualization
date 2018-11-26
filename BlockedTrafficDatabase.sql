# Recreate the database
CREATE DATABASE BlockedTrafficDatabase;

# For quick dropping
DROP DATABASE BlockedTrafficDatabase;

# Selecting the database for BlockedTraffic
USE BlockedTrafficDatabase;

# Setup for each of the tables inside the BlockedTraffic database

CREATE TABLE traffic(
  timeOf TIMESTAMP NOT NULL,
  protocol VARCHAR(50) NOT NULL,
  address VARCHAR(50) NOT NULL,
  PRIMARY KEY (address));
