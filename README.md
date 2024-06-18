# Conquest Server
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A python Fast API to serve [Conquest](https://github.com/brennenho/conquest), a chrome extension for USC students.


## Running Server
1. Copy `.env` values from [`.env.sample`](.env.sample)
2. `docker compose up -d`: start postgres database with Docker
3. `python3 -m venv venv`: create a virtual env
4. `pip install -r requirements.txt`: install server dependencies
5. `pip install -r requirements-dev.txt`: install developer tools (optional)
6. `make runuvicorn`: start Fast API on port 3002