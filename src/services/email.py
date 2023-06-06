from flask_mail import Message
from flask import url_for
from api import mail
from flask import Flask

def send_email(app: Flask, token: str, email: str, subject: str, endpoint: str) -> None:
    
    msg: Message = Message(
        subject,
        recipients=[email],
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    
    link: str = url_for(f'auth_bp.{endpoint}', token=token, _external=True)
    msg.body = f'Verification link {link}'
    mail.send(msg)
