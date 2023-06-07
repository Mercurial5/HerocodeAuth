from datetime import timedelta
from typing import Optional, Tuple, Dict, Any
from flask import session, jsonify
from flask_jwt_extended import create_access_token
from repositories.user_repository import find_user_by_email, update_last_login
from models.user import User


def authenticate(email: str, password: str)-> Optional[User]:
    user: Optional[User] = find_user_by_email(email)
    if user and user.verify_password(password):
        return user
    return None

def login_controller(data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    if 'email' not in data or "password" not in data:
        return jsonify({'message': 'Please provide credentials'}), 401
    
    email: str = data['email']
    password: str = data['password']

    user: Optional[User] = authenticate(email, password)
    
    if 'username' in session:
        return jsonify({'message': 'You are already logged in'}), 200
    
    if user:
        update_last_login(user)
        
        session['username'] = user.username
        access_token: str = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401
