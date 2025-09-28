FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

RUN mkdir /app/media

COPY . ./

EXPOSE 8000

