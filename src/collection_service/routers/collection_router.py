from datetime import date
import logging
from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Header, status, Depends, Query
from dependencies.auth_dependency import get_user_by_telegram_id_dependency
from schemas.schemas import (
    CollectionRequest,
    CollectionFilters,
    CollectionResponse,
    User,
)
from services.collection_service import CollectionService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/collections",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def get_all_collections_with_filters(
    filters: CollectionFilters = Depends(),
    collection_service: CollectionService = Depends(),
) -> List[CollectionResponse]:
    logger.debug(filters)
    res = await collection_service.get_all(filters)
    return res


@router.get(
    "/collections/{id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def get_collection_by_id(
    id: UUID,
    collection_service: CollectionService = Depends(),
) -> CollectionResponse:
    res = await collection_service.get(id)
    return res


@router.post(
    "/collections",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def create_collection(
    collection: CollectionRequest,
    user: User = Depends(get_user_by_telegram_id_dependency),
    collection_service: CollectionService = Depends(),
) -> CollectionResponse:
    new_collection = await collection_service.create(user, collection)
    return new_collection


@router.put(
    "/collections/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def update_collection(
    id: UUID,
    collection: CollectionRequest,
    user: User = Depends(get_user_by_telegram_id_dependency),
    collection_service: CollectionService = Depends(),
) -> None:
    await collection_service.update(user, id, collection)


@router.delete(
    "/collections/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def delete_collection(
    id: UUID,
    user: User = Depends(get_user_by_telegram_id_dependency),
    collection_service: CollectionService = Depends(),
) -> None:
    await collection_service.delete(user, id)
