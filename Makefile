include .env

# Start the server locally using Uvicorn on port 3002 with automatic reloading
# Make sure to start the postgres database with `make db`
local:
	uvicorn app.main:app --port 3002 --reload

# Build the server Docker image
# Rebuilding should only be necessary if dependencies or Docker setup changes
# Make sure to rebuild image for production
build:
	docker compose build
	docker image prune -f

# Start the server in a Docker container on port 8000
# Make sure to set the `TARGET` env variable
# TARGET=development: development server using Uvicorn with automatic reloading
# TARGET=production: production server using Gunicorn
docker:
	docker compose up -d

# Stop all Docker containers
stop:
	docker compose down

# Start the Postgres database in a Docker container
db:
	docker compose up conquest-db -d