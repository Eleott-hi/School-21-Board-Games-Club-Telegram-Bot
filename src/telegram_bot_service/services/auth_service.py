import httpx

from fastapi import status
from config import AUTH_SERVICE_HOST, AUTH_SERVICE_PORT, AUTH_SERVICE_VERSION


class AuthService:
    def __init__(self):
        self.auth_url = f"http://{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}/api/v{AUTH_SERVICE_VERSION}"

    async def is_registered(self, telegram_id: int):
        url = f"{self.auth_url}/user"
        headers = {"X-Telegram-ID": str(telegram_id)}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.status_code == status.HTTP_200_OK

    async def register(self, nickname: str, telegram_id: int):
        url = f"{self.auth_url}/register"
        headers = {"X-Telegram-ID": str(telegram_id)}
        payload = {"nickname": nickname}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            return response.status_code == status.HTTP_202_ACCEPTED

    async def confirm_token(self, token: str, telegram_id: int):
        url = f"{self.auth_url}/confirm_token"
        headers = {"X-Telegram-ID": str(telegram_id)}
        payload = {"token": token}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            return response.status_code == status.HTTP_202_ACCEPTED
