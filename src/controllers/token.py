from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from typing import Optional


def generate_confirmation_token(email: str) -> str:
    serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token: str, expiration: int=3600) -> Optional[str] :
    serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email: str = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return None

    return email