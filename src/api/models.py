from datetime import datetime
import bcrypt
from api import db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    last_login = db.Column(db.DateTime(), default=datetime.now())
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), default=datetime.now())


    def hash_password(self, plain_text_password):
        self.password = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, plain_text_password):
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), self.password.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.username}>'
    