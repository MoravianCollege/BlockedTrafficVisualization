import socket
import sys
import requests
import threading
import pymysql

# Create a TCP/IP socket for receiving data
RCV_UDP_IP = "10.230.1.59"
RCV_UDP_PORT = 5140

# Bind the socket to the port
rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
rcv_sock.bind((RCV_UDP_IP, RCV_UDP_PORT))

# Set up database connection
host = 'localhost'
database = 'BlockedTrafficDatabase'
user = 'root'

# connects to the database
conn = pymysql.connect(host=host, user=user, db=database)

# Thread that constantly collects data
def collect_data():
    while True:
        # Receive message
        data, address = rcv_sock.recvfrom(1024)

        # Parse up the message
        message = data.split(",")
        store_data(message)

# Stores the data from the collector thread into the database
def store_data(data):
    # Timestamp of the attack
    time = data[0]
    # IP address of the attack
    address = data[1]
    # Protocol (UDP or TCP)
    protocol = data[2]
    
    try:
        cursor = conn.cursor()

        # mysql statement
        traffic_add_sql = 'INSERT INTO traffic VALUES (%s, %s, %s)'

        # execution statement
        cursor.execute(traffic_add_sql, (time, address, protocol))
        conn.commit()
        conn.close()

    except:
        print("This piece of data failed to store: " + data)

# Start the collector thread
 data_collection_thread = Thread(target = collect_data)
 data_collection_thread.start()
