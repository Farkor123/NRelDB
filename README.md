# docker_flask_cassandra_example
================================
    
A sample Python Flask application using Cassandra and Docker containers.
*Using the **default** docker machine name for non-swarm deployment*

## Quick Start
-------------------------

* Docker Compose:

    `cd /pathto/NRelDB`
    
	`sudo docker-compose up`

* Verify:

	`chrome 0.0.0.0:5000`

## Development Configuration:
-------------------------

* Cassandra Docker container:

	`sudo docker run -d --name flask_cassandra -p 9042:9042 -t cassandra:3.11.4`

* Python Virtualenv:

   	`mkvirtualenv docker_flask_cassandra_example -r requirements.txt`

* Python Flask application:

	`CASSANDRA_PORT_9042_TCP_ADDR=$(docker-machine ip default) CASSANDRA_PORT_9042_TCP_PORT=9042 python app.py`
