include .env

runuvicorn:
	uvicorn app.main:app --port 3002 --reload