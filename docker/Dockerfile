FROM python:3.11.4-slim-bullseye AS prod

WORKDIR /app/src
COPY pyproject.toml poetry.lock /app/src/

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* && \
    pip install poetry==1.4.2 && \
    poetry config virtualenvs.create false && \
    poetry install --only main && \
    apt-get remove -y gcc \
    && rm -rf /var/lib/apt/lists/*

# Copying actual application
COPY . /app/src/