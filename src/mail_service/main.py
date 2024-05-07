from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from email.message import EmailMessage
import aiosmtplib
import asyncio
from schemas.schemas import EmailInfo, NearestEvents
import former
from pydantic import EmailStr

from services.mail_service import MailService

app: FastAPI = FastAPI(
    title="mailing", description="Service to manage mailing", version="0.0.1"
)

router: APIRouter = APIRouter()


@app.post("/", status_code=201)
async def parse_data(request: NearestEvents) -> None:
    """
    Asynchronously parses the incoming request and sends emails to users whose events are starting or ending soon.

    Args:
        request (NearestEvents): The incoming request containing user data and event information.

    Returns:
        None
    """
    data = request.model_dump()

    start_tasks: list = [
        send_mail(chunk["user"]["email"], former.form_string(former.TimeType.START))
        for chunk in data["starts_soon"]
    ]
    end_tasks: list = [
        send_mail(chunk["user"]["email"], former.form_string(former.TimeType.END))
        for chunk in data["ends_soon"]
    ]

    start_tasks += end_tasks

    if start_tasks:
        await asyncio.gather(*start_tasks)


async def send_mail(mail: str, message: str) -> None:
    """
    Asynchronously sends an email with the specified mail and message.

    Args:
        mail (str): The email address to send the email to.
        message (str): The message content of the email.

    Returns:
        None
    """


@app.post("/send", status_code=status.HTTP_202_ACCEPTED)
async def send_one_message(
    email_message: EmailInfo, mail_service: MailService = Depends()
) -> None:
    try:
        await mail_service.send_mail(email_message.email, email_message.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
