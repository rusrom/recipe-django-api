FROM python:3.7-alpine
MAINTAINER rusrom

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && mkdir /app && adduser -D user
USER user

WORKDIR /app
COPY ./app /app
