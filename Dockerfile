FROM python:3.8.7-slim
#3.8.7-alpine
#ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal postgresql-client
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY ./app /app

#RUN adduser user
#USER user