import httpx

from fastapi import HTTPException, status
from schemas.schemas import User
from config import AUTH_SERVICE_HOST, AUTH_SERVICE_PORT, AUTH_SERVICE_VERSION
import core.utils as utils


class AuthService:
    def __init__(self):
        self.auth_url = f"http://{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}/api/v{AUTH_SERVICE_VERSION}"

    async def is_registered(self, telegram_id: int) -> bool:
        url = f"{self.auth_url}/user"
        headers = {"X-Telegram-ID": str(telegram_id)}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.status_code == status.HTTP_200_OK

    async def register(self, nickname: str, telegram_id: int) -> bool:
        url = f"{self.auth_url}/register"
        headers = {"X-Telegram-ID": str(telegram_id)}
        payload = {"nickname": nickname}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            return response.status_code == status.HTTP_202_ACCEPTED

    async def confirm_token(
        self, token: str, telegram_id: int
    ) -> tuple[bool, str | None]:

        url = f"{self.auth_url}/confirm_token"
        headers = {"X-Telegram-ID": str(telegram_id)}
        payload = {"token": token}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code != status.HTTP_201_CREATED:
                return False, response.text

            return True, None

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """
        Requires:
            X-Telegram-ID header with Telegram ID
        Returns:
            User
        Exceptions local:
            HTTP_504_GATEWAY_TIMEOUT
            HTTP_401_UNAUTHORIZED
        """
        url = f"{self.auth_url}/user"
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)

            if response.status_code == 200:
                return User.model_validate_json(response.text)

            err = utils.get_fastapi_error(response)
            raise err

        except httpx.TimeoutException as err:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT)
