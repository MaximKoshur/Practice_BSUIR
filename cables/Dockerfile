FROM python:3.11-slim

RUN apt-get update

RUN pip install --upgrade pip

COPY ./pyproject.toml ./poetry.lock ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

ADD . .

WORKDIR /src