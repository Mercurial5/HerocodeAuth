import re


def is_valid_password(password: str) -> bool | str:
    MIN_LENGTH: int = 8
    MAX_LENGTH: int = 64

    if len(password) < MIN_LENGTH or len(password) > MAX_LENGTH:
        return "Password must be between 8 and 64 characters long"

    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter"

    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."

    return True


def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False
