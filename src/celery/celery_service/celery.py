from __future__ import absolute_import
from celery import Celery
import celeryconfig


# app = Celery()
# app.config_from_object(celeryconfig)

app = Celery('tasks',
            broker='amqp://guest:password@localhost/guest_vhost',
            backend='rpc://',
            include=['tasks'])