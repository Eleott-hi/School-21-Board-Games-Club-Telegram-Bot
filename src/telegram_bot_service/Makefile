export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build

all: init_timesone install wait_for_it run

init_timesone:
	date

install:
	pip install -r requirements.txt

wait_for_it: 
	chmod +x ./wait-for-it.sh 
	./wait-for-it.sh -t 120 $$MONGODB_SERVICE_HOST:$$MONGODB_SERVICE_PORT -- \
	./wait-for-it.sh -t 120 $$AUTH_SERVICE_HOST:$$AUTH_SERVICE_PORT -- 	     \
	./wait-for-it.sh -t 120 $$GAME_SERVICE_HOST:$$GAME_SERVICE_PORT


run:
	python3 main.py
