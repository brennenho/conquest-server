include .env

dev:
	uvicorn app.main:app --port 3002 --reload

prod:
	docker compose up --build -d
	docker image prune -f

stop:
	docker compose down