from flask import g, request, current_app


def login_required(view_func):
    def wrapper(*args, **kwargs):
        # 4. 判断用户登陆状态
        if g.user_id:
            token = request.headers.get("Authorization")[7:]
            key = "token:{}".format(g.user_id)
            token2 = current_app.redis_master.get(key)
            if token2 and token2.decode() != token:
                return {"message": "用户已经在其他设备登陆"}, 403

            return view_func(*args, **kwargs)
        else:
            return {"message": "用户未登录"}, 401

    return wrapper
