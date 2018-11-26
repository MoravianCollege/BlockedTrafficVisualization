from flask import Flask
from flask import request
import json
import pymysql
import os
import datetime

app = Flask(__name__)

@app.route('/')
def connect():
    return 'Hello, add a query onto the URL to get data.'

# Get all the attacks after a specified timestamp
@app.route('/getData', methods=['GET', 'POST'])
def getData():

    timestamp = request.args.get('timestamp')
    print(timestamp)

    server = 'localhost'
    database = 'BlockedTrafficDatabase'
    user = 'root'
    password = 'traffic'

    # database connection
    conn = pymysql.connect(host=server, user=user, password=password, db=database)
    cursor = conn.cursor()

    sql = 'SELECT timeOf, address, protocol FROM traffic WHERE timeOf >= ' + '"' + timestamp + '"' 
    cursor.execute(sql)
    attacks = []
    for attack in cursor:
        attacks.append(attack)

    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    return json.dumps(attacks, default = myconverter)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
