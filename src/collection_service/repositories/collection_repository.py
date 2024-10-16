from datetime import date
import logging
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.Collection import Collection
from database.database import get_session
from schemas.schemas import CollectionFilters, CollectionRequest

logger = logging.getLogger(__name__)


class CollectionRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
    ):
        self.session = session

    async def get(self, id: UUID) -> Collection | None:
        q = select(Collection).where(Collection.id == id)

        try:
            res = await self.session.execute(q)

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        res = res.scalars().first()
        if res is None:
            raise HTTPException(status_code=404, detail="Collection not found")

        return res

    async def get_all(self, filters: CollectionFilters) -> List[Collection]:
        q = select(Collection)

        if filters.user_id:
            q = q.where(Collection.user_id == filters.user_id)
        if filters.game_id:
            q = q.where(Collection.game_id == filters.game_id)
        if filters.type:
            q = q.where(Collection.type == filters.type)

        try:
            res = await self.session.execute(q)

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return res.scalars().all()

    async def create(self, user_id: UUID, collection: CollectionRequest) -> Collection:
        try:
            res = await self.get_all(
                filters=CollectionFilters(
                    game_id=collection.game_id,
                    user_id=user_id,
                )
            )

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        if res:
            print(res, flush=True)
            raise HTTPException(status_code=409, detail="Collection already exists")

        new_collection = Collection(**collection.model_dump(), user_id=user_id)

        self.session.add(new_collection)

        try:
            await self.session.commit()
            await self.session.refresh(new_collection)

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return new_collection

    async def delete(self, id: UUID) -> None:
        q = delete(Collection).where(Collection.id == id)

        try:
            await self.session.execute(q)
            await self.session.commit()

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update(self, id: UUID, collection: CollectionRequest) -> None:
        q = (
            update(Collection)
            .where(Collection.id == id)
            .values(**collection.model_dump(exclude_none=True))
        )

        try:
            await self.session.execute(q)
            await self.session.commit()

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
