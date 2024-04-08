all: init_timezone install wait_for_it run

init_timezone:
	date

wait_for_it: 
	chmod +x ./wait-for-it.sh 
	./wait-for-it.sh -t 120 postgres_service:5432 -- \
	./wait-for-it.sh -t 120 auth_service:8000

install:
	pip install -r requirements.txt

run:
	python3 main.py