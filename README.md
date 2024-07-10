# Conquest Server
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A python Fast API to serve [Conquest](https://github.com/brennenho/conquest), a chrome extension for USC students.


## Installing Server for local development
1. Install [pyenv](https://github.com/pyenv/pyenv) to manage python versions
2. Copy `.env` values from [`.env.sample`](.env.sample)
3. `python3 -m venv venv`: create a virtual env
4. `source venv/bin/activate`: activate virtual env
5. `pip install -r requirements.txt`: install server dependencies
6. `pip install -r requirements-dev.txt`: install developer tools (optional)

## Running Server
- Development: `make dev` (port 3002)
- Production: `make prod` (port 8000)
