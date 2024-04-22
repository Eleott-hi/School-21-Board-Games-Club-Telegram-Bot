FROM python:3.11

WORKDIR /app

COPY requirements.txt /app

EXPOSE 8001:8000

RUN apt-get update && apt-get upgrade -y  
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /app/requirements.txt