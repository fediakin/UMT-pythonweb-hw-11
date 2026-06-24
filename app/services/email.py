import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from dotenv import load_dotenv

from app.core.security import create_email_token

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", "test@example.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 465)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", ""),
    MAIL_FROM_NAME="Contacts App",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

async def send_email(email: EmailStr, host: str):
    try:
        token = create_email_token({"sub": email})
        html_content = f"""
        <html>
            <body>
                <h2>Вітаємо у нашому сервісі контактів!</h2>
                <p>Щоб завершити реєстрацію та підтвердити свою електронну адресу, будь ласка, перейдіть за посиланням нижче:</p>
                <a href="{host}auth/verify/{token}">Підтвердити Email</a>
            </body>
        </html>
        """
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            body=html_content,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message)
    except ConnectionErrors as err:
        print(f"Email sending error: {err}")