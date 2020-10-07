from flask import request, current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


# 登陆装饰器
def jwt_authentication():
    # print("登陆装饰器")
    # 1. 获取token
    token = request.headers.get("Authorization")
    # print(token)
    # 2. 判断token 是否有效
    payload = None
    if token and token.startswith("Bearer "):
        serializer = Serializer(secret_key=current_app.config.get("SECRET_KEY"),
                                expires_in=current_app.config.get("TOKEN_HOURS"))
        try:
            payload = serializer.loads(token[7:])
        except SignatureExpired:
            payload = None
        except BadSignature:
            payload = None

    # 3. 设置g.user_id
    g.user_id = None
    if payload:
        g.user_id = payload.get("user_id")
