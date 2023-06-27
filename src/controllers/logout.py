from typing import Tuple, Dict, Any
from flask import session
from flask import jsonify


def logout_controller() -> Tuple[Dict[str, Any], int]:
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'Successfuly logged out!'}), 200
