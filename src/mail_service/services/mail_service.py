import aiosmtplib as smtp

from email.message import EmailMessage
from config import MAIL_PASSWORD, MAIL_ADDRESS
from schemas.schemas import EmailInfo


class MailService:

    async def send_mail(self, email_info: EmailInfo) -> None:
        email = EmailMessage()
        email["From"] = MAIL_ADDRESS
        email["To"] = email_info.email
        email["Subject"] = email_info.subject
        email.set_content(email_info.message)

        print(email)

        tmp = await smtp.send(
            email,
            hostname="smtp.mail.ru",
            port=465,
            use_tls=True,
            username=MAIL_ADDRESS,
            password=MAIL_PASSWORD,
            timeout=10,
        )

        print(tmp)
