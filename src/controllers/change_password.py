from typing import Optional, Dict, Any, Tuple
from flask import jsonify, session
from repositories.user_repository import find_user_by_username, set_password, verify_pass
from models.user import User
from controllers.validator import is_valid_password


def change_password_controller(data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    if 'username' not in session:
        return jsonify({'message': 'Please login first'}), 401
    
    user: Optional[User] = find_user_by_username(session['username'])

    if not user:
        return jsonify({'message': 'User data not found'}), 404
    
    if 'old_password' not in data or 'new_password' not in data:
        return jsonify({'message': 'Provide old and new passwords'}), 401
    
    old_password: str = data['old_password']
    new_password: str = data['new_password']
    
    if not verify_pass(user, old_password):
        return jsonify({'message': 'Wrong password'}), 400

    if verify_pass(user, new_password):
        return jsonify({'message': 'New password cannot be the same as the old password'}), 400
    
    isvalid: bool | str = is_valid_password(new_password)
    if isvalid != True:
        return {'message': isvalid}, 400

    set_password(user, new_password)

    return jsonify({'message': 'Password changed successfully'}), 200