import socket
import sys
import requests
from flask import Flask, request
import threading
import datetime
import mysql.connector

# Create a TCP/IP socket for receiving data
RCV_UDP_IP = "10.230.1.59"
RCV_UDP_PORT = 5140

# Bind the socket to the port
rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
rcv_sock.bind((RCV_UDP_IP, RCV_UDP_PORT))

app = Flask(__name__)


q=[] #replace with database
mydb = mysql.connector.connect(
  host="localhost",
  user="testUser",
  passwd="somekindapassword"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE BlockedTrafficDatabase;")
mycursor.execute("USE BlockedTrafficDatabase;")

#Our database stores said data
mycursor.execute(
    "CREATE TABLE traffic(time VARCHAR(50) NOT NULL, protocol VARCHAR(50) NOT NULL, address VARCHAR(50) NOT NULL, PRIMARY KEY (address));")

def collect_data():
    while True:
        # Receive message
        data, address = rcv_sock.recvfrom(1024)

        # Parse original message and create a new one
        syslogmsg = data.split(",")
        store_data(syslogmsg)

def store_data(data):
    #timestamp of the attack
    time = data[0]
    #address of the attack
    address = data[1]
    #protocol (UDP or TDP)
    protocol = data[2]

    #Our database stores said data
    try:
        sql = "INSERT INTO traffic (time, protocol, address) VALUES (%s, %s, %s);"
        val = (time, protocol, address)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
    except:
        print("This piece of data failed to store: " + data)

@ app.route('/timestamp')
def getAllSince():
    timestamp = request.args.get('t')
    list_of_attacks = []
    sql = "Select * FROM traffic WHERE time = '" + timestamp+ "';"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        list_of_attacks.append(x)
    return str(list_of_attacks)


if __name__ == "__main__":
    data_collection_thread = threading.Thread(target=collect_data)
    data_collection_thread.start()
    app.run(host="0.0.0.0", port=5000)


