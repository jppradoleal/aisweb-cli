FROM python:3.10 AS base
WORKDIR /app
EXPOSE 8000

FROM python:3.10 AS build
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry
RUN poetry install
COPY . .
ENTRYPOINT [ "./run.sh" ]
