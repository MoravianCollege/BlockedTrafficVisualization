import socket
import sys
from flask import Flask, request
from threading import Thread
import redis
# Create a TCP/IP socket for receiving data
RCV_UDP_IP = "10.230.1.59"
RCV_UDP_PORT = 5140

# Bind the socket to the port
rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
rcv_sock.bind((RCV_UDP_IP, RCV_UDP_PORT))
app = Flask(__name__)
ip_addresses = {}
call_made = False
def aggregate_data():
    while not call_made:
        # Receive message
        data, address = rcv_sock.recvfrom(1024)
 	    # add IP to running list
        syslogmsg = data.split(",")
        #ip_list.append(syslogmsg[1])

        ip = syslogmsg[1]
        if ip in ip_addresses:
            ip_addresses[ip] +=1
        else:
            ip_addresses[ip] = 1


@app.route('/aggregate')
def send_data():
    call_made = True
    num_ips = int(request.args.get('num_ips'))
    sorted_ips = sorted(ip_addresses, key=ip_addresses.__getitem__, reverse=Tru$
    ips_to_be_sent = []
    for i in range(num_ips):
        ips_to_be_sent.append(sorted_ips[i])
	return str(ips_to_be_sent)

if __name__ == "__main__":
    data_aggregation_thread = Thread(target = aggregate_data)
    data_aggregation_thread.start()
    app.run(host="0.0.0.0", port=5000)