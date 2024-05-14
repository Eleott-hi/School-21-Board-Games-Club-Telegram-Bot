from datetime import datetime, timedelta
from typing import Dict
import jwt

from fastapi import Depends, HTTPException
from models.User import AuthMethod
from repositories.auth_repository import AuthRepository
from schemas.auth_schemas import ConfirmSchema, RegisterSchema, User
from services.mail_service import MailService
from services.redis_service import RedisService
from config import SERVICE_SECRET_KEY, SERVICE_SECRET_ALGORITHM, CONFIRMATION_TOKEN_TTL


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

    async def start_registeration(self, register_schema: RegisterSchema):
        nickname = register_schema.nickname
        telegram_id = register_schema.telegram_id
        email = self.get_email_address_from_nickname(nickname)
        token = self.encode_jwt({"nickname": nickname})

        await self.mail_service.send_token(email=email, token=token)

        await self.redis_service.set(
            key=nickname, value=telegram_id, ttl=CONFIRMATION_TOKEN_TTL
        )

    async def confirm_token(self, confirm_schema: ConfirmSchema):
        payload = self.decode_jwt(confirm_schema.token)
        nickname = payload["nickname"]
        telegram_id = await self.redis_service.get(nickname)
        email = self.get_email_address_from_nickname(nickname)

        if not telegram_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        await self.redis_service.delete(nickname)

        await self.auth_repository.add(
            telegram_id=telegram_id,
            nickname=nickname,
            email=email,
            auth_method=AuthMethod.TELEGRAM,
        )

    async def get_user_by_telegram_id(self, telegram_id: int) -> User:
        user = await self.auth_repository.get_by_telegram_id(telegram_id=telegram_id)
        return User.model_validate(user)

    def get_email_address_from_nickname(self, nickname: str):
        return f"{nickname}@student.school-21.ru"

    def decode_jwt(self, token: str):
        try:
            return jwt.decode(
                jwt=token,
                key=SERVICE_SECRET_KEY,
                algorithms=[SERVICE_SECRET_ALGORITHM],
            )

        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")

    def encode_jwt(self, payload: Dict):
        return jwt.encode(
            payload={
                **payload,
                "exp": int(
                    (
                        datetime.now() + timedelta(seconds=CONFIRMATION_TOKEN_TTL)
                    ).timestamp()
                ),
            },
            key=SERVICE_SECRET_KEY,
            algorithm=SERVICE_SECRET_ALGORITHM,
        )
