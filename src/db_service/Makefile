all: init_timezone run

init_timezone:
	date

run:
	if [ -z "${MODE}" ]; then\
		python3 main.py;\
	else\
		pytest;\
	fi