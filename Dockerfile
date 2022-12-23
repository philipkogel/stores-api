FROM python:3.11.1-alpine3.17
LABEL maintainer="philipkogel"

ENV PYTHONUNBUFFERED 1

COPY ./app /app
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements-dev.txt /app/requirements-dev.txt

WORKDIR /app

EXPOSE 8000
ARG DEV=false

RUN python3 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip freeze > requirements.txt && \
    if [ $DEV = "true" ]; \
      then pip install -r /app/requirements-dev.txt ; \
    fi