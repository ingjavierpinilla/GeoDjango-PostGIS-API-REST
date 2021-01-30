FROM python:3.9-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt-get autoremove -y gcc

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser user
USER user