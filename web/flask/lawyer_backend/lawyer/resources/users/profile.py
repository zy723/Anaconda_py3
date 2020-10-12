from flask import g
from flask_restful import Resource

from common.cache.user import UserCache
from common.utils.login_required import login_required


class UserInfoResource(Resource):
    """
    用户中心
    """
    method_decorators = {
        "get": [login_required]
    }

    def get(self):
        user_dict = UserCache(g.user_id).get()

        if not user_dict:
            return None

        return user_dict
