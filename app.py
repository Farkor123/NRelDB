# pylint: disable=broad-except,invalid-name
"""
    Sample Flask app testing Cassandra connection
"""
import os
from datetime import datetime
from flask import Flask, jsonify, request
import json

from cassandra.cluster import Cluster
from cassandra.query import ordered_dict_factory

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
        "CREATE KEYSPACE IF NOT EXISTS pollution WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")
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
    data = request.data
    data_dict = json.loads(data.decode('utf-8'))
    date = data_dict['date']
    time = data_dict['time']
    location = data_dict['location']
    if date is None or time is None or location:
        return "<html><body><h1>Fields cannot be empty!</h1></body></html>"
    else:
        columns = str(data_dict.keys()).replace("'", "")[1:-1]
        values = str(data_dict.values())[1:-1]
        query = "INSERT INTO plays (" + columns + ") VALUES (" + values + ")"
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
