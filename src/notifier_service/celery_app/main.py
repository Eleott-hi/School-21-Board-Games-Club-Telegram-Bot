from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab



app = Celery('tasks',
            broker_url='redis://localhost:6379',
            result_backend='redis://localhost:6379')





app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Novosibirsk',
    enable_utc=True
)

app.conf.beat_schedule = {
    'fetch-data': {
        'task': 'app.tasks.fetch_data_wrapper',
        'schedule': crontab(minute='*/5'),
    }
}


