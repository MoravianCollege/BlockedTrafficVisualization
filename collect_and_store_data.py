
import socket
import sys
import requests
import threading
import pymysql
import datetime

# Create a TCP/IP socket for receiving data
RCV_UDP_IP = "10.230.1.59"
RCV_UDP_PORT = 5140

# Bind the socket to the port
rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
rcv_sock.bind((RCV_UDP_IP, RCV_UDP_PORT))

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
        # Set up database connection
        host = 'localhost'
        database = 'BlockedTrafficDatabase'
        user = 'root'
        password = 'traffic'

        # connects to the database
        conn = pymysql.connect(host=host, user=user, password=password, db=database)

        # Check if timestamp is valid
        times = time.split(" ")
        if times[0][4] == "/" and times[0][7] == "/" and times[1][2] == ":" and times[1][5] == ":":
            # Check if IP address is valid
            if socket.inet_aton(address):
                # Check if protocol is valid
                if protocol == "tcp" or protocol == "udp" or protocol == "icmp":
                    # Create MySQL cursor
                    cursor = conn.cursor()

                    # mysql statement
                    traffic_add_sql = 'INSERT INTO traffic VALUES (%s, %s, %s)'

                    # execution statement
                    cursor.execute(traffic_add_sql, (time, address, protocol))
                    conn.commit()
                    conn.close()

    except:
        print("Not added to the database: ", data)

collect_data()

       
