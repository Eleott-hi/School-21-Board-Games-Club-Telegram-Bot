all: install wait_for_it run

wait_for_it:
	chmod +x ./wait-for-it.sh
	./wait-for-it.sh -t 120 redis_service:6379 -- \
	./wait-for-it.sh -t 120 telegram_service:8000 -- \

install:
	pip install -r requirements.txt

run:
	celery -A celery_app worker --beat --loglevel=info