from passlib.apps import custom_app_context as pwd_context
from api import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean()),
    last_login = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def hash_password(self, password) -> None:
        self.password = pwd_context.encrypt(password)
        
    def verify_password(self, password) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def __repr__(self):
        return f'<User {self.username}>'
    