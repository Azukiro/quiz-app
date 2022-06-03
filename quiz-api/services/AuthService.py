from helpers import jwt_utils as jwt
PASSWORD = "Steve"


def verify_token(headers):
    auth = headers.get('Authorization')
    if auth is None:
        return False
    token = auth.split()[1]
    login = jwt.decode_token(token)
    if login != 'quiz-app-admin':
        return False
    return True


def login(password):
    if password == PASSWORD:
        return jwt.build_token()
    else:
        raise ValueError("Invalid password")
