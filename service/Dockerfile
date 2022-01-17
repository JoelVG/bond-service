FROM python:3.8.12-alpine3.14

WORKDIR /app

COPY requirements.txt /app/

ENV PORT=8000

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /app/