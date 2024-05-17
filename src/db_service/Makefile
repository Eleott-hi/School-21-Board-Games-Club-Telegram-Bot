all: wait_for_it run

wait_for_it: 
	chmod +x ./wait-for-it.sh 
	./wait-for-it.sh -t 120 postgres_service:5432

run:
	if [ -z "${MODE}" ]; then\
		python3 main.py;\
	else\
		pytest;\
	fi