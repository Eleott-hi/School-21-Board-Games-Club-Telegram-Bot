# HINT: use and modify this file only if you use database.py and related folder as independent application
from dotenv import load_dotenv
import os
import pytz

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

AUTH_SERVICE = os.getenv("AUTH_SERVICE")

GOOGLE_TOKEN=os.getenv("GOOGLE_TOKEN")
AUTHORIZED_USER=os.getenv("AUTHORIZED_USER")
