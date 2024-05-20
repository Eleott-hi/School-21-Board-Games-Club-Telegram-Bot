from fastapi import APIRouter, Depends, status
from schemas.auth_schemas import ConfirmSchema, RegisterSchema, User
from services.auth_service import AuthService

router = APIRouter(
    tags=["auth"],
    responses={401: {"description": "Not authorized"}},
)


@router.post(
    "/register",
    status_code=status.HTTP_202_ACCEPTED,
)
async def register(
    register_schema: RegisterSchema,
    auth_service: AuthService = Depends(),
):
    print(register_schema)
    await auth_service.start_registeration(register_schema)


@router.post(
    "/confirm_token",
    status_code=status.HTTP_201_CREATED,
)
async def confirm_token(
    confirm_schema: ConfirmSchema,
    auth_service: AuthService = Depends(),
):
    await auth_service.confirm_token(confirm_schema)


@router.get(
    "/user/{telegram_id}",
    status_code=status.HTTP_200_OK,
)
async def get_user(
    telegram_id: int,
    auth_service: AuthService = Depends(),
) -> User:
    return await auth_service.get_user_by_telegram_id(telegram_id)
