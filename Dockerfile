FROM python:3.7-alpine
MAINTAINER rusrom

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client \
    && apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev \
    && pip install -r /requirements.txt \
    && apk del .tmp-build-deps \
    && mkdir /app \
    && adduser -D user
USER user

WORKDIR /app
COPY ./app /app
