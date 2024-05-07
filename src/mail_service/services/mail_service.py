from email.message import EmailMessage
import aiosmtplib


class MailService:
    
    async def send_mail(self, mail: str, message: str) -> None:
        email = EmailMessage()
        email["From"] = "not_reply@bytecode.su"
        email["To"] = mail
        email["Subject"] = "Booking_S21_notify"
        email.set_content(message)

        tmp = await aiosmtplib.send(
            email,
            hostname="smtp.mail.ru",
            port=465,
            use_tls=True,
            username="not_reply@bytecode.su",
            password="rhDM2eyJeHxNRbkjk72C",
        )

        print(tmp)
