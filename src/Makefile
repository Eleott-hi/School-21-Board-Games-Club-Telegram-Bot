DB_DIR := postgres_service
DB_CONTAINER_NAME := postgres_service

all:  clean_db up

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs

clean_db:
	-docker stop $(DB_CONTAINER_NAME)
	-docker rm $(DB_CONTAINER_NAME)

ngrok:
	docker run --net=host -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest http 4040

prune:
	docker system prune -a