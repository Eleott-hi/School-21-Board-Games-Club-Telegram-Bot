import aiosmtplib as smtp
import ssl

from email.message import EmailMessage

from fastapi import HTTPException, status
from config import MAIL_PASSWORD, MAIL_ADDRESS
from schemas.schemas import EmailInfo


class MailService:
    def __init__(self):
        self.smtp = "smtp.mail.ru"

    async def send_mail(self, email_info: EmailInfo) -> None:
        """
        Sends an email using SMTP.

        This function sends an email to the recipient specified in the EmailInfo object.
        Note: This function does not work when connected through a VPN.

        Args:
            email_info (EmailInfo): An object containing the email recipient's address,
                                    subject, and message body.

        Raises:
            SMTPException: If there is an error sending the email.

        Example:
            email_info = EmailInfo(
                email="recipient@example.com",
                subject="Test Subject",
                message="This is a test message."
            )
            await self.send_mail(email_info)
        """
        email = EmailMessage()
        email["From"] = MAIL_ADDRESS
        email["To"] = email_info.email
        email["Subject"] = email_info.subject
        email.set_content(email_info.message)

        try:
            await smtp.send(
                email,
                hostname=self.smtp,
                port=465,
                use_tls=True,
                username=MAIL_ADDRESS,
                password=MAIL_PASSWORD,
                timeout=10,
            )
        except smtp.errors.SMTPConnectTimeoutError as e:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e)
            )
