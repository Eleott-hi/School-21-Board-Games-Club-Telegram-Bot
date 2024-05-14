from config import MAIL_SERVICE_URL
from httpx import AsyncClient


class MailService:

    def __init__(self):
        self.url = MAIL_SERVICE_URL

    async def send_token(self, email, token):
        async with AsyncClient() as client:
            res = await client.post(
                self.url + "/send_email",
                json={
                    "email": email,
                    "subject": "Confirm registration",
                    "message": f"Token:\n{token}",
                },
                timeout=10,
            )
