export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build

all: init_timesone install run

init_timesone:
	date

install:
	pip install -r requirements.txt

run:
	python3 main.py

freeze:
	pip freeze > requirements.txt