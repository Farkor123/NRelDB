"""
    Sample Flask app testing Cassandra connection
"""
import os
from datetime import datetime
from flask import Flask, jsonify, request
import json
from cassandra.cluster import Cluster

app = Flask(__name__)

cluster = Cluster([os.environ.get('CASSANDRA_PORT_9042_TCP_ADDR', 'localhost')],
                  port=int(os.environ.get('CASSANDRA_PORT_9042_TCP_PORT', 9042)))


@app.route('/')
def index():
    try:
        session = cluster.connect()
    except Exception as error:
        message = "%s: %s" % (error.__class__.__name__, str(error))
        return jsonify(message=message, hostname=os.uname()[1],
                       current_time=str(datetime.now())), 500
    session.execute(
        "CREATE KEYSPACE IF NOT EXISTS pollution WITH replication = "
        "{'class':'SimpleStrategy', 'replication_factor' : 3};")
    session.execute("CREATE TABLE IF NOT EXISTS pollution.data("
                    "location text,"
                    "date date,"
                    "time time,"
                    "carbon_oxide double,"
                    "tin_oxide double,"
                    "nmhc double,"
                    "benzene double,"
                    "titania double,"
                    "nox double,"
                    "tungsten_oxide double,"
                    "indium_oxide double,"
                    "temperature double,"
                    "relative_humidity double,"
                    "absolute_humidity double,"
                    "PRIMARY KEY (location, date, time)"
                    ")")
    session.execute("INSERT INTO pollution.data(location, date, time) "
                    "VALUES ('Lodz', '2019-04-24','13:30:54')")
    return 'Hello World'


@app.route('/end')
def end():
    try:
        session = cluster.connect()
    except Exception as error:
        message = "%s: %s" % (error.__class__.__name__, str(error))
        return jsonify(message=message, hostname=os.uname()[1],
                       current_time=str(datetime.now())), 500
    session.execute("DROP KEYSPACE IF EXISTS pollution;")
    return 'Goodbye World'


@app.route('/crud', methods=['POST'])
def create():
    try:
        session = cluster.connect()
    except Exception as error:
        message = "%s: %s" % (error.__class__.__name__, str(error))
        return jsonify(message=message, hostname=os.uname()[1],
                       current_time=str(datetime.now())), 500
    data_dict = request.args
    date = data_dict.get('date')
    time = data_dict.get('time')
    location = data_dict.get('location')
    print(date, time, location)
    if date is None or time is None or location is None:
        return "<html><body><h1>Fields cannot be empty!</h1></body></html>"
    else:
        columns, values = '', ''
        for i in data_dict.keys():
            columns += str(i) + ', '
        for i in data_dict.values():
            values += "'" + str(i) + "'" + ', '
        values = values[:-2]
        columns = columns[:-2]
        query = "INSERT INTO pollution.data (" + columns + ") VALUES (" + values + ")"
        session.execute(query)
        return "<html><body><h1>Success</h1></body></html>"


@app.route('/crud', methods=['GET'])
def read():
    try:
        session = cluster.connect()
    except Exception as error:
        message = "%s: %s" % (error.__class__.__name__, str(error))
        return jsonify(message=message, hostname=os.uname()[1],
                       current_time=str(datetime.now())), 500
    data_dict = request.args
    date = data_dict.get('date')
    time = data_dict.get('time')
    location = data_dict.get('location')
    print(date, time, location)
    if date is None or time is None or location is None:
        return "<html><body><h1>Fields cannot be empty!</h1></body></html>"
    else:
        query = "SELECT * FROM pollution.data " \
                "WHERE date = '" + date + "' " \
                "AND time = '" + time + "' " \
                "AND location = '" + location + "';"
        ret = ""
        for i in session.execute(query):
            for j in i:
                ret += str(j) + ', '
        return ret[:-2]


@app.route('/crud', methods=['PUT'])
def update():
    try:
        session = cluster.connect()
    except Exception as error:
        message = "%s: %s" % (error.__class__.__name__, str(error))
        return jsonify(message=message, hostname=os.uname()[1],
                       current_time=str(datetime.now())), 500


@app.route('/crud', methods=['DELETE'])
def delete():
    try:
        session = cluster.connect()
    except Exception as error:
        message = "%s: %s" % (error.__class__.__name__, str(error))
        return jsonify(message=message, hostname=os.uname()[1],
                       current_time=str(datetime.now())), 500


if __name__ == '__main__':
    # Connect via 0.0.0.0:8000
    app.run(host='0.0.0.0', debug=True)
