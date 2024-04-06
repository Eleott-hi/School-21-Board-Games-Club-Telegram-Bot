FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

RUN apt-get update && apt-get upgrade -y  
RUN apt-get install -y make  
RUN python3 -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt
