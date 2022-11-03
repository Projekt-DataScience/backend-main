FROM python:3.10.0-alpine
COPY requirements.txt requirements.txt
RUN apk add --update libpq-dev
RUN pip install -r requirements.txt