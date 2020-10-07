from flask import g


def login_required(view_func):
    def wrapper(*args, **kwargs):
        # 4. 判断用户登陆状态
        if g.user_id:
            return view_func(*args, **kwargs)
        else:
            return {"message": "用户未登录"}, 401

    return wrapper
