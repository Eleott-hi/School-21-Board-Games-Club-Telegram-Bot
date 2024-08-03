from fastapi import status
from datetime import date
from typing import Optional
from urllib.parse import urlencode
from uuid import UUID
import httpx
from pydantic import BaseModel
from core.Exceptions import TelegramException, TelegramExceptions
from enum import Enum as PyEnum

from config import (
    COLLECTION_SERVICE_HOST,
    COLLECTION_SERVICE_PORT,
    COLLECTION_SERVICE_VERSION,
)
import core.utils as utils


class CollectionType(str, PyEnum):
    BLACK_LIST = "black_list"
    FAVORITE = "favorite"


class CollectionRequest(BaseModel):
    game_id: UUID
    type: CollectionType


class CollectionFilters(BaseModel):
    game_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    type: Optional[CollectionType] = None


class CollectionService:
    def __init__(self):
        self.base_url = f"http://{COLLECTION_SERVICE_HOST}:{COLLECTION_SERVICE_PORT}/api/v{COLLECTION_SERVICE_VERSION}"

    async def get_collections(self, filters: dict = None):
        url = f"{self.base_url}/collections"

        if filters:
            filters = CollectionFilters(**filters).model_dump(exclude_unset=True)
            
            if "type" in filters:
                filters["type"] = filters["type"].value

            url += f"?{urlencode(filters)}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == status.HTTP_200_OK:
                return response.json()

            err = utils.get_fastapi_error(response)
            print("Error:", err, flush=True)

        raise TelegramException(TelegramExceptions.UNKNOWN_EXCEPTION)

    async def create_collection(
        self, telegram_id: int, game_id: UUID, type: CollectionType
    ):
        url = f"{self.base_url}/collections"
        headers = {"Telegram-ID": str(telegram_id)}
        payload = dict(game_id=game_id, type=type)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == status.HTTP_201_CREATED:
                return response.json()

            if response.status_code == status.HTTP_409_CONFLICT:
                raise TelegramException(
                    exception_type=TelegramExceptions.COLLECTION_ALREADY_EXISTS_EXCEPTION
                )

            err = utils.get_fastapi_error(response)
            print("Error:", err, flush=True)

        raise TelegramException(TelegramExceptions.UNKNOWN_EXCEPTION)

    async def delete_collection(self, telegram_id: int, collection_id: UUID):
        url = f"{self.base_url}/collections/{str(collection_id)}"
        headers = {"Telegram-ID": str(telegram_id)}

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
            if response.status_code == status.HTTP_204_NO_CONTENT:
                return

            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise TelegramException(
                    exception_type=TelegramExceptions.COLLECTION_NOT_FOUND_EXCEPTION
                )

            err = utils.get_fastapi_error(response)
            print("Error:", err, flush=True)

        raise TelegramException(TelegramExceptions.UNKNOWN_EXCEPTION)
