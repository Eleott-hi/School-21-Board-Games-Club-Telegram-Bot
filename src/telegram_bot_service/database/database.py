import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient as MDB
from config import MONGODB_SERVICE_URL


client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_SERVICE_URL)
database = client.telegram_db
