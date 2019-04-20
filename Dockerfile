################################################################################
##  Name:   Dockerfile
##  Date:   2019-04-20
##  Developer:  Adam Sadowski
##  Email:  210310@edu.p.lodz.pl
##  Purpose:   This Dockerfile contains the Docker builder commands for a simple
##	Flask application.
################################################################################
FROM python:3.6-slim
MAINTAINER Adam Sadowski

# install the python requirements
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

## run the app
ADD app.py app.py

## expose the port
EXPOSE 5000

## start the command
CMD ["python", "app.py"]