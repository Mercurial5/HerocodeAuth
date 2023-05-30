from datetime import datetime
from flask import Blueprint
from flask import request, jsonify
from flask import current_app
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

    send_email(current_app, token, email, subject)

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
