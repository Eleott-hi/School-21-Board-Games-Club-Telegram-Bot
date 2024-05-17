# TelegramBot-BoardGameClub
Telegram bot for Board Game Club in School 21, Novosibirsk

for initial launch of database:
- **docker-compose up**
- **docker-compose exec db_service alembic revision --autogenerate -m "revision_number"**
- **docker-compose exec db_service alembic upgrade head**

Then, if you want to fill games with apporpriate data, just do:
- **docker-compose exec db_service python3 filling_data.py**

