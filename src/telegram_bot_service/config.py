from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_API_URL = os.getenv("DB_API_URL")
PAGINATION_LIMIT = 5

