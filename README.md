# Project Title

Crooked Cooks Flask Server interface

## Getting Started

This repo contains the API exposed by our Python Flask server for interaction with the PostgreSQL database.
*This is an academic project, which is why things like direct URLs to the postgresql server are uploaded. A deployment/commercial product would, naturally, maintain it off-public-repo, since this is a potential security loophole.

### Prerequisites

Pip packages within the requirements.txt file
PostgreSQL 9.6 installed on your computer, for the psycopg2 package to work

### Installing

Install PostgreSQL 9.6 on your computer. Relevant download links for different Operating Systems can be found at https://www.postgresql.org/download/.
Install the relevant Python packages via pip install -r /path/to/requirements.txt

## Features
A suite of the API functionalities can be found on https://docs.google.com/spreadsheets/d/1yVGgf84yc4FbcBoM5QxjwzSaOsayuK390SyjBT0zg1k/edit?usp=sharing, using HTTP GET and POST requests for different functions.
Concurrency is managed by psycopg2, and can (as of now) manage up to 20 concurrent requests - a limitation of Amazon RDS's Free Tier.

## Running the tests

Run testapp.py, which will automatically cycle through different functionalities of the API to verify their respective functionalities.

## Deployment

One can run a local server which interacts with the Amazon RDS database by executing application.py. Connecting to localhost:5000/api/[api_function] would then be able to interface with the PostgreSQL server.

## Built With

* Python 3.6 - psycopg2, Flask
* Heroku - Flask/gunicorn
* Amazon RDS - PostgreSQL

## To be developed
Main functionality of the necessary API is developed; additional work would be focused on refinement, eg. developing more tests, and user-testing, to see if any more features are required.

## Authors

* **Tze How** - *Initial work* - [Tzeusy](https://github.com/Tzeusy)

## Acknowledgments

* Professors Sudipta and Sun Jun (SUTD), course leads for the 50.003 module.
* Udemy, for nice PostgreSQL/Flask tutorials
