MONGO_DB_CONTAINER_NAME := mongodb_service 
POSTGRES_CONTAINER_NAME := postgres_service

all: stop clean_db up

up:
	docker-compose up

stop:
	docker-compose stop

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

freeze:
	docker exec auth_service make freeze
	docker exec mail_service make freeze
	docker exec telegram_bot_service make freeze
	docker exec booking_service make freeze
	docker exec game_service make freeze
	docker exec collection_service make freeze

init_db:
	docker exec game_service make init_db
