from typing import List, Dict
import asyncio



def async_wait(time: int = 2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(time)
            res = await func(*args, **kwargs)
            return res

        return wrapper
    return decorator