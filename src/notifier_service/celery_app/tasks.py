from celery import shared_task
from aiohttp import ClientSession
import asyncio



async def fetch_data():
    data_source_url = (

    )

    tg_notifier_url = (

    )

    try:
        async with ClientSession() as session:
            async with session.get(data_source_url) as response:
                data = await response.json()

            async with session.post(utl=tg_notifier_url, json=data) as response:
                tg_response = await response.json()

    except Exception as e:
        print(e)

@shared_task
def fetch_data_wropper():
    asyncio.run(fetch_data())


# start with persistent storage
# docker run --rm --name some-redis -d redis redis-server --save 60 1 --loglevel warning

