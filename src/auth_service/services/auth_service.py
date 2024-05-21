from typing import Dict

from fastapi import Depends, HTTPException
from models.User import AuthMethod
from repositories.auth_repository import AuthRepository
from schemas.auth_schemas import ConfirmSchema, RegisterSchema, User
from services.mail_service import MailService
from services.redis_service import RedisService
from config import CONFIRMATION_TOKEN_TTL
from utils.JWT import decode_jwt, encode_jwt


class AuthService:

    def __init__(
        self,
        redis_service: RedisService = Depends(),
        mail_service: MailService = Depends(),
        auth_repository: AuthRepository = Depends(),
    ):
        self.redis_service = redis_service
        self.mail_service = mail_service
        self.auth_repository = auth_repository

    async def start_registeration(
        self,
        telegram_id: int,
        nickname: str,
    ):
        email = self.get_email_address_from_nickname(nickname)
        token = encode_jwt({"nickname": nickname})

        await self.mail_service.send_token(email=email, token=token)

        await self.redis_service.set(
            key=nickname,
            value=telegram_id,
            ttl=CONFIRMATION_TOKEN_TTL,
        )

    async def confirm_token(
        self,
        telegram_id: int,
        token: str,
    ):
        payload = decode_jwt(token)
        nickname = payload["nickname"]
        email = self.get_email_address_from_nickname(nickname)

        radis_telegram_id = await self.redis_service.get(nickname)
        if not radis_telegram_id:
            raise HTTPException(status_code=400, detail="Invalid token")

        radis_telegram_id = int(radis_telegram_id)
        if radis_telegram_id != telegram_id:
            raise HTTPException(
                status_code=400, detail="Token was sent from another telegram id"
            )

        await self.redis_service.delete(nickname)

        await self.auth_repository.add(
            telegram_id=int(radis_telegram_id),
            nickname=nickname,
            email=email,
            auth_method=AuthMethod.TELEGRAM,
        )

    async def get_user_by_telegram_id(self, telegram_id: int) -> User:
        user = await self.auth_repository.get_by_telegram_id(telegram_id=telegram_id)
        return User.model_validate(user)

    def get_email_address_from_nickname(self, nickname: str):
        return f"{nickname}@student.21-school.ru"
