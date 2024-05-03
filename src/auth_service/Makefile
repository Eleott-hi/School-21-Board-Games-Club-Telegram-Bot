export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build

all: init_timesone install wait_for_it run

init_timesone:
	date

install:
	pip install -r requirements.txt

wait_for_it: 
	chmod +x ./wait-for-it.sh 

run:
	python3 main.py
