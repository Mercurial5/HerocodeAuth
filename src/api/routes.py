from datetime import datetime, timedelta
from flask import Blueprint
from flask import request, jsonify
from flask import current_app, session
from flask_jwt_extended import create_access_token
from api.token import generate_confirmation_token
from api.redis_db import get_redis_connection
from api.models import User
from api.email import send_email
from api import db


auth_bp = Blueprint("auth_bp", __name__, url_prefix='/api/v1')

@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    if 'username' not in data:
        return {'message': 'Username field cant be empty'}, 400
    if 'email' not in data:
        return {'message': 'Email field cant be empty'}, 400
    if 'password' not in data:
        return {'message': 'Write password'}, 400


    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return {'message': 'Username already taken'}, 409
    if User.query.filter_by(email=email).first():
        return {'message': 'Email already taken'}, 409

    subject = "Please confirm your email"
    token = generate_confirmation_token(email)

    redis_conn = get_redis_connection()
    redis_key = f'{token}'
    redis_data = {
        'username': username,
        'email': email,
        'password': password
    }
    redis_conn.hmset(redis_key, redis_data)
    redis_conn.expire(redis_key, current_app.config['REDIS_EXPIRATION'])

    send_email(current_app, token, email, subject, 'register_verify')

    return jsonify({'message': 'Registration successful'}), 200


@auth_bp.route('/register-verify', methods=['GET'])
def register_verify():
    token = request.args.get('token')

    if not token:
        return jsonify({'message': 'Token is missing'}), 400
    redis_conn = get_redis_connection()
    redis_key = f'{token}'
    redis_data_in_bytes = redis_conn.hgetall(redis_key)
    redis_data = {key.decode(): value.decode() for key, value in redis_data_in_bytes.items()}
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


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return user
    return False


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'email' not in data or "password" not in data:
        return jsonify({'message': 'Please provide credentials'}), 401
    
    email = data['email']
    password = data['password']

    user = authenticate(email, password)
    
    if 'username' in session:
        return jsonify({'message': 'You are already logged in'})
    
    if user:
        user.last_login=datetime.now()
        db.session.commit()

        session['username'] = user.username
        expires = timedelta(days=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401
    

@auth_bp.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'Successfuly logged out!'})


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()

    if 'email' not in data:
        return jsonify({'message': 'Please provide Email'}), 401
    
    email = data['email']
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not registered, please sign up first'}), 404
    
    token = generate_confirmation_token(email)

    redis_conn = get_redis_connection()
    redis_key = f'{token}'
    redis_data = {
        'email': email,
        'reset_token': token
    }
    redis_conn.hmset(redis_key, redis_data)
    redis_conn.expire(redis_key, current_app.config['REDIS_EXPIRATION'])

    subject = "Please click here to reset password"

    send_email(current_app, token, email, subject, 'change_password')

    return jsonify({'message': 'Password changed successfully'})


@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    token = request.args.get('token')

    if not token:
        return jsonify({'message': 'Please check your email'}), 400
    if 'new_password' not in data:
        return jsonify({'message': 'Please provide new password'}), 400
    
    new_password = data['new_password']
    
    redis_conn = get_redis_connection()
    redis_key = f'{token}'
    redis_data_in_bytes = redis_conn.hgetall(redis_key)
    redis_data = {key.decode(): value.decode() for key, value in redis_data_in_bytes.items()}

    if not redis_data:
        return jsonify({'message': 'User data not found'}), 404
    
    if not redis_data.get('reset_token'):
        return jsonify({'message': 'Reset password to change'})
   
    user = User.query.filter_by(email=redis_data.get('email')).first()
    if user.verify_password(new_password):
        return jsonify({'message': 'New password cannot be the same as the old password'}), 400
    user.hash_password(new_password)
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200