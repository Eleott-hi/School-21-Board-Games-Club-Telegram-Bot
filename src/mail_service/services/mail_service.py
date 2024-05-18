import aiosmtplib as smtp

from email.message import EmailMessage
from config import MAIL_PASSWORD, MAIL_ADDRESS


class MailService:

    async def send_mail(self, to: str, subject: str, message: str) -> None:
        email = EmailMessage()
        email["From"] = MAIL_ADDRESS
        email["To"] = to
        email["Subject"] = subject
        email.set_content(message)

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
