# Recreate the database
CREATE DATABASE BlockedTrafficDatabase;

# Selecting the database for BlockedTraffic
USE BlockedTraffic;

# Setup for each of the tables inside the BlockedTraffic database

CREATE TABLE traffic(
  data        VARCHAR(200) NOT NULL,
  ipAddress   VARCHAR(50) NOT NULL,

  PRIMARY KEY (ipAddress)
);
