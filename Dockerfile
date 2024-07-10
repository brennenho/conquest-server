FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./conquest-server/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./conquest-server/app /app/app