MONGO_DB_CONTAINER_NAME := mongodb_service 
POSTGRES_CONTAINER_NAME := postgres_service

all: down up

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs

clean_db:
	-docker stop $(MONGO_DB_CONTAINER_NAME)
	-docker rm   $(MONGO_DB_CONTAINER_NAME)
	-docker stop $(POSTGRES_CONTAINER_NAME)
	-docker rm   $(POSTGRES_CONTAINER_NAME)

ngrok:
	docker run --net=host -it -e NGROK_AUTHTOKEN=xyz ngrok/ngrok:latest http 4040

prune:
	docker system prune -a