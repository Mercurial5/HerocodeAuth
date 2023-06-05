from datetime import datetime, timedelta
from typing import Tuple, Dict, Any, Optional
from flask import Blueprint
from flask import request, jsonify
from flask import current_app, session
from flask_jwt_extended import create_access_token
from redis import Redis
from api.token import generate_confirmation_token
from api.redis_db import get_redis_connection
from api.models import User
from api.email import send_email
from api import db
from api.validator import is_valid_password, is_valid_email


auth_bp = Blueprint("auth_bp", __name__, url_prefix='/api/v1')

@auth_bp.route('/register', methods=['POST'])
def register() -> Tuple[Dict[str, Any], int]:
    data: Dict[str, Any] = request.get_json()

    if 'username' not in data:
        return {'message': 'Username field cant be empty'}, 400
    if 'email' not in data:
        return {'message': 'Email field cant be empty'}, 400
    if 'password' not in data:
        return {'message': 'Write password'}, 400

    username: str = data.get('username')
    email: str = data.get('email')
    password: str = data.get('password')

    if User.query.filter_by(username=username).first():
        return {'message': 'Username already taken'}, 409
    if User.query.filter_by(email=email).first():
        return {'message': 'Email already taken'}, 409

    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email address'}), 400
    
    isvalid: bool | str = is_valid_password(password)
    if isvalid != True:
        return {'message': f'{isvalid}'}, 400

    subject: str = "Please confirm your email"
    token: str = generate_confirmation_token(email)

    redis_conn: Redis = get_redis_connection()
    redis_key: str = token
    redis_data: Dict[str, str] = {
        'username': username,
        'email': email,
        'password': password
    }
    redis_conn.hmset(redis_key, redis_data)
    redis_conn.expire(redis_key, current_app.config['REDIS_EXPIRATION'])

    send_email(current_app, token, email, subject, 'register_verify')

    return jsonify({'message': 'Check your email for verification'}), 200


@auth_bp.route('/register-verify', methods=['GET'])
def register_verify() -> Tuple[Dict[str, Any], int]:
    token: str = request.args.get('token')

    if not token:
        return jsonify({'message': 'Token is missing'}), 400
    
    redis_conn: Redis = get_redis_connection()
    redis_key: str = token
    redis_data_in_bytes = redis_conn.hgetall(redis_key)
    redis_data: Dict[str, str] = {key.decode(): value.decode() for key, value in redis_data_in_bytes.items()}

    if not redis_data:
        return jsonify({'message': 'User data not found'}), 404
    
    if redis_data.get('verified') == 'True':
        return jsonify({'message': 'User already verified!'}), 400

    user = User(
        username=redis_data.get('username'),
        email=redis_data.get('email'),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    user.hash_password(redis_data.get('password'))
    db.session.add(user)
    db.session.commit()

    redis_conn.hset(redis_key, 'verified', 'True')

    return jsonify({'message': 'User verified!!!'}), 200


def authenticate(email: str, password: str)-> Optional[User]:
    user: Optional[User] = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return user
    return None


@auth_bp.route('/login', methods=['POST'])
def login() -> Tuple[Dict[str, Any], int]:
    data: Dict[str, Any] = request.get_json()

    if 'email' not in data or "password" not in data:
        return jsonify({'message': 'Please provide credentials'}), 401
    
    email: str = data['email']
    password: str = data['password']

    user: Optional[User] = authenticate(email, password)
    
    if 'username' in session:
        return jsonify({'message': 'You are already logged in'})
    
    if user:
        user.last_login=datetime.now()
        db.session.commit()

        session['username'] = user.username
        expires: timedelta = timedelta(days=1)
        access_token: str = create_access_token(identity=str(user.id), expires_delta=expires)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401
    

@auth_bp.route('/logout')
def logout() -> Tuple[Dict[str, Any], int]:
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'Successfuly logged out!'})


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password() -> Tuple[Dict[str, Any], int]:
    data: Dict[str, Any] = request.get_json()

    if 'email' not in data or 'new_password' not in data:
        return jsonify({'message': 'Please provide Email and New password'}), 401
    
    email: str = data['email']
    new_password: str = data['new_password']
    user: Optional[User] = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'Not any user registered by this email'}), 404
    
    if user.verify_password(new_password):
        return jsonify({'message': 'New password cannot be the same as the old password'}), 400
    
    isvalid: bool | str = is_valid_password(new_password)
    if isvalid != True:
        return {'message': f'{isvalid}'}, 400
    
    token: str = generate_confirmation_token(email)
    
    redis_conn: Redis = get_redis_connection()
    redis_key: str = token
    redis_data: Dict[str, str] = {
        'email': email,
        'new_password': new_password
    }
    redis_conn.hmset(redis_key, redis_data)
    redis_conn.expire(redis_key, current_app.config['REDIS_EXPIRATION'])

    subject: str = "Please click here to reset password"

    send_email(current_app, token, email, subject, 'reset_password_verify')

    return jsonify({'message': 'Check your email for verification'})


@auth_bp.route('/reset-password/verify')
def reset_password_verify() -> Tuple[Dict[str, Any], int]:
    token: str = request.args.get('token')

    if not token:
        return jsonify({'message': 'Please check your email'}), 400

    redis_conn: Redis = get_redis_connection()
    redis_key: str = token
    redis_data_in_bytes = redis_conn.hgetall(redis_key)
    redis_data: Dict[str, str] = {key.decode(): value.decode() for key, value in redis_data_in_bytes.items()}

    if not redis_data:
        return jsonify({'message': 'Validation link expired'}), 404
    
    if redis_data.get('reset') == 'True':
        return jsonify({'message': 'Your password has already been reset'}), 200

    email: str = redis_data.get('email')
    new_password: str = redis_data.get('new_password')

    user: Optional[User] = User.query.filter_by(email=email).first()
    user.hash_password(new_password)
    db.session.commit()

    redis_conn.hset(redis_key, 'reset', 'True')
    
    return jsonify({'message': 'Password changed successfully'}), 200


@auth_bp.route('/change-password', methods=['POST'])
def change_password() -> Tuple[Dict[str, Any], int]:
    if request.method == 'POST':
        if 'username' not in session:
            return jsonify({'message': 'Please login first'}), 401
        
        user: Optional[User] = User.query.filter_by(username=session['username']).first()
        if not user:
            return jsonify({'message': 'User data not found'}), 404
        
        data: Dict[str, Any] = request.get_json()
        if 'old_password' not in data or 'new_password' not in data:
            return jsonify({'message': 'Provide old and new passwords'}), 401
        
        old_password: str = data['old_password']
        new_password: str = data['new_password']
        
        if not user.verify_password(old_password):
            return jsonify({'message': 'Wrong password'}), 400

        if user.verify_password(new_password):
            return jsonify({'message': 'New password cannot be the same as the old password'}), 400
        
        isvalid: bool | str = is_valid_password(new_password)
        if isvalid != True:
            return {'message': f'{isvalid}'}, 400

        user.hash_password(new_password)
        db.session.commit()

        return jsonify({'message': 'Password changed successfully'}), 200
