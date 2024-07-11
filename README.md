# Conquest Server
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A python Fast API to serve [Conquest](https://github.com/brennenho/conquest), a chrome extension for USC students.


## Install development requirements
1. Install [pyenv](https://github.com/pyenv/pyenv) to manage python versions
2. Install [Docker compose](https://docs.docker.com/compose/install/)
3. Copy `.env` values from [`.env.sample`](.env.sample)
4. `python3 -m venv venv`: create a virtual env
5. `source venv/bin/activate`: activate virtual env
6. `pip install -r requirements.txt`: install server dependencies
7. `pip install -r requirements-dev.txt`: install developer tools (optional)

### Run local development server
- `make db`: start postgres database with Docker
- `make local`: start local Uvicorn server on port `3002`

### Run Dockerized development server
- Set env variable `TARGET=development`
- `make build`: build Docker image
    - Rebuilding the image is only needed if the dependencies or Docker setup changes
- `make docker`: up Docker container with a Uvicorn server on port `8000`

> [!NOTE]
> Both development servers automatically reload when any changes are made in the `/app` folder

### Run Dockerized production server
- Set env variable `TARGET=production`
- `make build`: build Docker image
    - The image must be rebuilt on any change
- `make docker`: up Docker container with a Gunicorn server running multiple workers on port `8000`