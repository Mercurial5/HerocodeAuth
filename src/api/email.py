from flask_mail import Message, Mail
from flask import url_for


mail = Mail()

def send_email(app, token, email, subject):
    mail.init_app(app)

    msg = Message(
        subject,
        recipients=[email],
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )

    
    link = url_for('auth_bp.register_verify', token=token, _external=True)
    msg.body = f'Verification link {link}'
    mail.send(msg)
