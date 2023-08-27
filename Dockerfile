FROM python:slim

RUN \
    pip install Sanga

WORKDIR /app
