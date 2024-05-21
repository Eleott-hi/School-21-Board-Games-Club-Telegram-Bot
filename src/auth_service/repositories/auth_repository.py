from fastapi import HTTPException
from models.User import AuthMethod, User
from database.database import get_session, select
from schemas.auth_schemas import User as PyUser


class AuthRepository:

    async def add(
        self,
        telegram_id: int,
        nickname: str,
        email: str,
        auth_method: AuthMethod = AuthMethod.TELEGRAM,
    ):
        async with get_session() as session:
            session.add(
                User(
                    telegram_id=telegram_id,
                    nickname=nickname,
                    email=email,
                    auth_method=auth_method,
                )
            )
            await session.commit()

    async def get_by_telegram_id(self, telegram_id: int) -> User:
        async with get_session() as session:
            q = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(q)
            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return user

    # TEST
    class Utils:
        @classmethod
        async def get_by_telegram_id(cls, telegram_id: int) -> PyUser:
            async with get_session() as session:
                q = select(User).where(User.telegram_id == telegram_id)
                result = await session.execute(q)
                user = result.scalars().first()

                if not user:
                    raise HTTPException(status_code=404, detail="User not found")

                return PyUser.model_validate(user)
