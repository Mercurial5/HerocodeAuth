from typing import Optional, Dict
from datetime import datetime
from models.user import User
from api import db


def create_user(redis_data: Dict[str, str]) -> None:
    user: User = User(
        username=redis_data.get('username'),
        email=redis_data.get('email'),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    user.hash_password(redis_data.get('password'))
    db.session.add(user)
    db.session.commit()


def find_user_by_email(email) -> Optional[User]:
    return User.query.filter_by(email=email).first()


def find_user_by_username(username) -> Optional[User]:
    return User.query.filter_by(username=username).first()


def update_last_login(user) -> None:
    user.last_login=datetime.now()
    db.session.commit()


def set_password(user, password) -> None:
    user.hash_password(password)
    db.session.commit()


def verify_pass(user, password) -> bool:
    return user.verify_password(password)
