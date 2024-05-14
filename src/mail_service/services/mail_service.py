from email.message import EmailMessage
import aiosmtplib as smtp


class MailService:

    async def send_mail(self, to: str, subject: str, message: str) -> None:
        email = EmailMessage()
        email["From"] = "s21boardgamesclub@mail.ru"
        email["To"] = to
        email["Subject"] = subject
        email.set_content(message)

        print(email)

        tmp = await smtp.send(
            email,
            hostname="smtp.mail.ru",
            port=465,
            use_tls=True,
            username=email["From"],
            password="wyYbSgXHLeHu62DPniqa",
            timeout=10,
        )

        print(tmp)
