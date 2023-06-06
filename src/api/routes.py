from typing import Tuple, Dict, Any
from flask import Blueprint
from flask import request
from services.register import register_controller, register_verify_controller
from services.login import login_controller
from services.logout import logout_controller
from services.change_password import change_password_controller
from services.reset_password import reset_password_controller, reset_password_verify_controller


auth_bp = Blueprint("auth_bp", __name__, url_prefix='/api/v1')

@auth_bp.route('/register', methods=['POST'])
def register() -> Tuple[Dict[str, Any], int]:
    data: Dict[str, Any] = request.get_json()
    return register_controller(data)


@auth_bp.route('/register-verify', methods=['GET'])
def register_verify() -> Tuple[Dict[str, Any], int]:
    token: str = request.args.get('token')
    return register_verify_controller(token)


@auth_bp.route('/login', methods=['POST'])
def login() -> Tuple[Dict[str, Any], int]:
    data: Dict[str, Any] = request.get_json()
    return login_controller(data)
    

@auth_bp.route('/logout')
def logout() -> Tuple[Dict[str, Any], int]:
    return logout_controller()


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password() -> Tuple[Dict[str, Any], int]:
    data: Dict[str, Any] = request.get_json()
    return reset_password_controller(data)


@auth_bp.route('/reset-password/verify')
def reset_password_verify() -> Tuple[Dict[str, Any], int]:
    token: str = request.args.get('token')
    return reset_password_verify_controller(token)


@auth_bp.route('/change-password', methods=['POST'])
def change_password() -> Tuple[Dict[str, Any], int]:
    if request.method == 'POST':
        data: Dict[str, Any] = request.get_json()
        return change_password_controller(data)
