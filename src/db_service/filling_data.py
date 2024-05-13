import asyncio

from db.database import init_db

async def main():
    await init_db()

if __name__ == "__main__":
    asyncio.run(main())