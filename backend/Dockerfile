FROM python:3.8.5-slim

LABEL maintainer="artur-holubeu@yandex.by" version="1.0.0"

WORKDIR /backend

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn foodgram_api.wsgi:application --bind 0.0.0.0:8000