from dotenv import load_dotenv
import os
import pytz

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DRIVER = os.getenv("DB_DRIVER")

DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_USER_TWO = os.getenv("DB_USER_TWO")
DB_NAME_TWO = os.getenv("DB_NAME_TWO")
DB_PASSWORD_TWO = os.getenv("DB_PASSWORD_TWO")


DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL_TWO = f"{DB_DRIVER}://{DB_USER_TWO}:{DB_PASSWORD_TWO}@{DB_HOST}:{DB_PORT}/{DB_NAME_TWO}"


AUTH_SERVICE = os.getenv("AUTH_SERVICE")
