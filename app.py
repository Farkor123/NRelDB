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
                    "carbon_oxide text,"
                    "tin_oxide text,"
                    "nmhc text,"
                    "benzene text,"
                    "titania text,"
                    "nox text,"
                    "tungsten_oxide text,"
                    "indium_oxide text,"
                    "temperature text,"
                    "relative_humidity text,"
                    "absolute_humidity text,"
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
    if data_dict.get('date') is None \
            or data_dict.get('time') is None \
            or data_dict.get('location') is None:
        return "<html><body><h1>Fields cannot be empty!</h1></body></html>"
    else:
        query = "INSERT INTO pollution.data (" + \
                ', '.join(str(i) for i in data_dict.keys()) + \
                ") VALUES (" + \
                ', '.join("'" + str(i) + "'" for i in data_dict.values()) + \
                ")"
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
    if date is None or time is None or location is None:
        return "<html><body><h1>Fields cannot be empty!</h1></body></html>"
    else:
        ret = ', '.join(str(j) for j in [i for i in session.execute(
            "SELECT * FROM pollution.data WHERE " \
            "date = '" + date + "' AND " \
            "time = '" + time + "' AND " \
            "location = '" + location + "';"
        )])
        return ret[4:-1]


@app.route('/crud', methods=['PUT'])
def update():
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
    if date is None or time is None or location is None:
        return "<html><body><h1>Fields cannot be empty!</h1></body></html>"
    else:
        xD = ""
        for _ in list(zip([i for i in data_dict.keys()][3:], [i for i in data_dict.values()][3:])):
            xD += " = '".join(__ for __ in _) + "', "
        session.execute("UPDATE pollution.data SET " +\
            xD[:-2] +\
            " WHERE location = '" + location + "' AND " \
            "date = '" + date + "' AND " \
            "time = '" + time + "';")
        return 'Updated'


@app.route('/crud', methods=['DELETE'])
def delete():
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
    if date is None or time is None or location is None:
        return "<html><body><h1>Fields cannot be empty!</h1></body></html>"
    else:
        session.execute("DELETE FROM pollution.data WHERE "
                        "date = '" + date + "' AND "
                        "time = '" + time + "' AND "
                        "location = '" + location + "';")
        return 'Deleted'


if __name__ == '__main__':
    # Connect via 0.0.0.0:8000
    app.run(host='0.0.0.0', debug=True)
