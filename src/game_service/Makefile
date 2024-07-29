export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build

all: init_timesone install wait_for_it run
test: init_timesone install pytest

init_timesone:
	date

install:
	pip install -r requirements.txt

wait_for_it: 
	chmod +x ./wait-for-it.sh 
	./wait-for-it.sh -t 120 "$$POSTGRES_SERVICE_HOST:$$POSTGRES_SERVICE_PORT"

run:
	python3 main.py

pytest:
	pytest
