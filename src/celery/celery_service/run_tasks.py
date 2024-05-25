from __future__ import absolute_import
from celery_service.tasks import add


if __name__ == "__main__":
    result = add.delay(1, 2)
    print(result.ready())
    print(result.result)


# celery -A celery_service worker --loglevel=info