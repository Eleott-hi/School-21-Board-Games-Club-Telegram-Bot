from fastapi import APIRouter, Depends, Request, status
from schemas.auth_schemas import ConfirmSchema, RegisterSchema, User
from services.auth_service import AuthService
from routers.utils import get_telegram_id

router = APIRouter(
    prefix="/telegram",
    tags=["auth"],
    responses={401: {"description": "Not authorized"}},
)


@router.post(
    "/register",
    status_code=status.HTTP_202_ACCEPTED,
)
async def register(
    register_schema: RegisterSchema,
    telegram_id: int = Depends(get_telegram_id),
    auth_service: AuthService = Depends(),
):
    await auth_service.start_registeration(telegram_id, register_schema.nickname)


@router.post(
    "/confirm_token",
    status_code=status.HTTP_201_CREATED,
)
async def confirm_token(
    confirm_schema: ConfirmSchema,
    telegram_id: int = Depends(get_telegram_id),
    auth_service: AuthService = Depends(),
):
    await auth_service.confirm_token(telegram_id, confirm_schema.token)


@router.get(
    "/user/{telegram_id}",
    status_code=status.HTTP_200_OK,
)
async def get_user(
    telegram_id: int = Depends(get_telegram_id),
    auth_service: AuthService = Depends(),
) -> User:
    return await auth_service.get_user_by_telegram_id(telegram_id)
