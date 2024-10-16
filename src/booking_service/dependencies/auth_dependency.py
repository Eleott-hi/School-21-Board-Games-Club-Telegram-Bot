from fastapi import Header, Depends, HTTPException, Request
from services.auth_service import AuthService
from schemas.schemas import User


async def get_user_by_telegram_id_dependency(
    telegram_id: int = Header(),
    auth_service: AuthService = Depends(),
) -> User:
    user = await auth_service.get_user_by_telegram_id(telegram_id)
    return user
