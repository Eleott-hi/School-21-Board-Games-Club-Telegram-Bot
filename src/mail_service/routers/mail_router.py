from fastapi import APIRouter, status, Depends, HTTPException
from schemas.schemas import EmailInfo
from services.mail_service import MailService

router: APIRouter = APIRouter()


@router.post("/send_email", status_code=status.HTTP_202_ACCEPTED)
async def send_email(
    email_info: EmailInfo,
    mail_service: MailService = Depends(),
) -> None:

    try:
        await mail_service.send_mail(
            email_info.email,
            email_info.subject,
            email_info.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
