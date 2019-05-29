# docker_flask_cassandra_example
================================
    
A sample Python Flask application using Cassandra and Docker containers.
*Using the **default** docker machine name for non-swarm deployment*

## Quick Start
-------------------------

* Docker Compose:

    `cd /pathto/NRelDB`
    
	`sudo docker-compose up -d`

* Verify:

	`chrome 0.0.0.0:5000`
	
	check if docks are ok
	
	`chrome 0.0.0.0:10001`

## Development Configuration:
-------------------------
* Python Virtualenv:

   	`mkvirtualenv docker_flask_cassandra_example -r requirements.txt`

* Python Flask application:

	`app.py`
