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

prune:
	docker system prune -a

sed:
	find . -type f -name "*.sh" -exec sed -i 's/\r//g' {} +
