from typing import Optional, Tuple, Dict, Any
from flask import current_app
from flask import jsonify
from repositories.user_repository import create_user, find_user_by_email, find_user_by_username
from services.validator import is_valid_email, is_valid_password
from services.token import generate_confirmation_token
from services.email import send_email
from cache.cache_data import cache_user_data, get_cached_user_data, set_done, is_verified


def register_controller(data) -> Tuple[Dict[str, Any], int]:
    if 'username' not in data:
        return {'message': 'Username field cant be empty'}, 400
    if 'email' not in data:
        return {'message': 'Email field cant be empty'}, 400
    if 'password' not in data:
        return {'message': 'Write password'}, 400

    username: str = data.get('username')
    email: str = data.get('email')
    password: str = data.get('password')

    if find_user_by_username(username):
        return {'message': 'Username already taken'}, 409
    if find_user_by_email(email):
        return {'message': 'Email already taken'}, 409

    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email address'}), 400
    
    isvalid: bool | str = is_valid_password(password)
    if isvalid != True:
        return {'message': isvalid}, 400

    subject: str = "Please confirm your email"
    token: str = generate_confirmation_token(email)

    cache_data: Dict[str, str] = {
        'username': username,
        'email': email,
        'password': password
    }

    cache_user_data(token, cache_data)
    
    send_email(current_app, token, email, subject, 'register_verify')

    return jsonify({'message': 'Check your email for verification'}), 200


def register_verify_controller(token: str) -> Tuple[Dict[str, Any], int]:
    if not token:
        return jsonify({'message': 'Token is missing'}), 400
    
    cache_data: Optional[Dict[str, str]] = get_cached_user_data(token)
    if not cache_data:
        return jsonify({'message': 'User data not found'}), 404
    
    if is_verified(cache_data):
        return jsonify({'message': 'User already verified!'}), 400

    create_user(cache_data)

    set_done(token)

    return jsonify({'message': 'User verified!!!'}), 200
