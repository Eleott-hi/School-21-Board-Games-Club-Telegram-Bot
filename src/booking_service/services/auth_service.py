import httpx
import logging

from fastapi import HTTPException, status

from config.config import AUTH_SERVICE_HOST, AUTH_SERVICE_PORT, AUTH_SERVICE_VERSION
from schemas.schemas import User
from services import utils

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.auth_url = f"http://{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}/api/v{AUTH_SERVICE_VERSION}"

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        '''
        Requires:
            X-Telegram-ID header with Telegram ID
        Returns:
            User
        Exceptions local:
            HTTP_504_GATEWAY_TIMEOUT
            HTTP_401_UNAUTHORIZED
        '''
        url = f"{self.auth_url}/user"
        headers = {"X-Telegram-ID": str(telegram_id)}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                logger.debug(response)

            if response.status_code == 200:
                return User.model_validate_json(response.text)

            err = utils.get_fastapi_error(response)
            logger.error(err)
            raise err

        except httpx.TimeoutException as err:
            logger.error(err)
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT)
