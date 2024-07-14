# Get platform architecture from .env
ARG ARCH
ARG LOG_LEVEL

# Build base image
FROM --platform=linux/${ARCH} tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS base

WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

# Execute start scripts depending on environment
FROM base AS development
CMD ["/start-reload.sh"]

FROM base AS production
CMD ["/start.sh"]