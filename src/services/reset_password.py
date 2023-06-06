from typing import Optional, Dict, Tuple, Any
from flask import session, jsonify, current_app
from models.user import User
from services.validator import is_valid_password
from services.token import generate_confirmation_token
from services.email import send_email
from cache.cache_data import cache_user_data, get_cached_user_data, set_done
from repositories.user_repository import find_user_by_email, set_password, verify_pass


def reset_password_controller(data) -> Tuple[Dict[str, Any], int]:
    if 'username' in session:
        return jsonify({'message': 'You are logged in'}), 401
    
    if 'email' not in data or 'new_password' not in data:
        return jsonify({'message': 'Please provide Email and New password'}), 401
    
    email: str = data['email']
    new_password: str = data['new_password']
    user: Optional[User] = find_user_by_email(email)

    if not user:
        return jsonify({'message': 'Not any user registered by this email'}), 404
    
    if verify_pass(user, new_password):
        return jsonify({'message': 'New password cannot be the same as the old password'}), 400
    
    isvalid: bool | str = is_valid_password(new_password)
    if isvalid != True:
        return {'message': isvalid}, 400
    
    token: str = generate_confirmation_token(email)

    cache_data: Dict[str, str] = {
        'email': email,
        'new_password': new_password
    }
    cache_user_data(token, cache_data)

    subject: str = "Please click here to reset password"
    send_email(current_app, token, email, subject, 'reset_password_verify')

    return jsonify({'message': 'Check your email for verification'}), 200

def reset_password_verify_controller(token) -> Tuple[Dict[str, Any], int]:
    if not token:
        return jsonify({'message': 'Please check your email'}), 400
     
    cashed_data: Optional[Dict[str, str]] = get_cached_user_data(token)
    
    if not cashed_data:
        return jsonify({'message': 'Validation link expired'}), 404
    
    if cashed_data.get('reset') == 'True':
        return jsonify({'message': 'Your password has already been reset'}), 200

    email: str = cashed_data.get('email')
    new_password: str = cashed_data.get('new_password')

    user: Optional[User] = find_user_by_email(email)
    set_password(user, new_password)

    set_done(token, 'reset')
    
    return jsonify({'message': 'Password changed successfully'}), 200