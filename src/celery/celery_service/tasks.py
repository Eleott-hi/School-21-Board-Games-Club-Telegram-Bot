from celery import Celery

app = Celery('tasks',
             broker='amqp://guest:password@localhost/guest_vhost',
            #  broker='amqp://guest:password@rabbit_mq_service/guest_vhost',
             backend='rpc://',
            )

@app.task
def add(x, y):
    return x + y