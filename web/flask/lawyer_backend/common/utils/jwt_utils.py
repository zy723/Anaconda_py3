from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def generate_token(user_id, role, expires_in):
    serializer = Serializer(secret_key=current_app.config.get("SECRET_KEY"), expires_in=expires_in)
    token = serializer.dumps({
        "user_id": user_id,
        "role": role
    }).decode()
    return token
