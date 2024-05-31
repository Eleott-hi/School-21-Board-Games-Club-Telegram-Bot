from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab

from config import BROKER_URL, BACKEND_URL, TZ


app = Celery('tasks',
            broker_url=BROKER_URL,
            result_backend=BACKEND_URL)


app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone=TZ,
    enable_utc=True
)


app.conf.beat_schedule = {
    'fetch-data': {
        'task': 'app.tasks.fetch_data_wrapper',
        'schedule': crontab(minute='*/5'),
    }
}


