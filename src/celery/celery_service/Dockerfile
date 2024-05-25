FROM python:3.11-slim

WORKDIR /APP

COPY ./tasks.py .

RUN apt update -y && apt upgrade -y
RUN python3 -m pip install celery

EXPOSE 5672

CMD ["celery", "-A tasks worker", "--loglevel=INFO"]