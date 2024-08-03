from datetime import date
import logging
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from schemas.schemas import (
    CollectionFilters,
    CollectionResponse,
    CollectionRequest,
    User,
)
from services.auth_service import AuthService
from services.game_service import GamesService
from repositories.collection_repository import CollectionRepository

logger = logging.getLogger(__name__)


class CollectionService:
    def __init__(
        self,
        auth_service: AuthService = Depends(),
        game_service: GamesService = Depends(),
        collection_repository: CollectionRepository = Depends(),
    ):
        self.auth_service = auth_service
        self.game_service = game_service
        self.collection_repository = collection_repository

    async def get(self, id: UUID) -> CollectionResponse:
        res = await self.collection_repository.get(id)
        return CollectionResponse.model_validate(res)

    async def get_all(self, filters: CollectionFilters) -> List[CollectionResponse]:
        res = await self.collection_repository.get_all(filters)
        return [CollectionResponse.model_validate(r) for r in res]

    async def create(
        self,
        user: User,
        collection: CollectionRequest,
    ) -> CollectionResponse:
        _ = await self.game_service.get_game_by_id(collection.game_id)

        new_collection = await self.collection_repository.create(user.id, collection)
        return CollectionResponse.model_validate(new_collection)

    async def update(self, user: User, id: UUID, collection: CollectionRequest) -> None:
        db_collection = await self.get(id)
        if db_collection.user_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

        await self.collection_repository.update(id, collection)
        return

    async def delete(self, user: User, id: UUID) -> None:
        db_collection = await self.get(id)

        if db_collection.user_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

        await self.collection_repository.delete(id)
        return
