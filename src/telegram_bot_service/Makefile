all: init_timesone install wait_for_it run

init_timesone:
	date

install:
	pip install -r requirements.txt

wait_for_it: 
	chmod +x ./wait-for-it.sh 
#	./wait-for-it.sh -t 120 auth_service:8000

run:
	python3 main.py

grpc:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/auth.proto