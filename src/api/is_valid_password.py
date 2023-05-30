import re

def is_valid_password(password):
    MIN_LENGTH = 8
    MAX_LENGTH = 64

    if len(password) < MIN_LENGTH or len(password) > MAX_LENGTH:
        return "Password must at least 8 characters long"

    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter"

    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."

    if not re.search(r'\d', password):
        return "Password must contain at least one digit."

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."

    return True