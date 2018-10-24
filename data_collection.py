import socket
import sys
import requests
import Queue
from flask import Flask, request
import threading
import datetime

# Create a TCP/IP socket for receiving data
RCV_UDP_IP = "10.230.1.59"
RCV_UDP_PORT = 5140

# Bind the socket to the port
rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
rcv_sock.bind((RCV_UDP_IP, RCV_UDP_PORT))

app = Flask(__name__)

lock = threading.Lock()
q = []

def collect_data():
    while True:
        # Receive message
        data, address = rcv_sock.recvfrom(1024)
        #check if the other thread is using the list
        lock.acquire()
        for attack in q:
            syslogmsg = attack.split(",")
            attack_time = datetime.datetime.strptime(syslogmsg[0].replace(" ", ""), '%Y/%m/%d%H:%M:%S')
            if (attack_time < datetime.datetime.now() - datetime.timedelta(seconds=60)):
                q.remove(attack)
            # add data to the list
            q.append(data.replace(" ", ""))
            lock.release()

@ app.route('/timestamp')
def getAllSince():
    timestamp = request.args.get('t')
    lock.acquire()
    list_of_attacks = []
    timestamp = datetime.datetime.strptime(timestamp, '%Y/%m/%d%H:%M:%S')
    try:
        for attack in q:
            line = attack.split(",")
            attack_time = datetime.datetime.strptime(line[0], '%Y/%m/%d%H:%M:%S')
            if (attack_time > timestamp):
                list_of_attacks.append(attack)
    finally:
        lock.release()
    return str(list_of_attacks)


if __name__ == "__main__":
    data_collection_thread = threading.Thread(target=collect_data)
    data_collection_thread.start()
    app.run(host="0.0.0.0", port=5000)


