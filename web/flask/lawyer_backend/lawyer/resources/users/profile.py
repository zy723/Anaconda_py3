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
        user_info = UserCache(g.user_id).get()

        if not user_info:
            return None

        user_dict = {
            "user_name": user_info["name"],
            "user_photo_url": user_info["profile_photo"],
        }

        return user_dict


class UserDetailsResource(Resource):
    """
    个人中心-详细
    """
    method_decorators = {
        "get": [login_required]
    }

    def get(self):
        user_info = UserCache(g.user_id).get()

        if not user_info:
            return None

        user_dict = {
            "mobile": user_info["mobile"],
            "user_photo_url": user_info["profile_photo"],
            "user_name": user_info["name"],
            "company": user_info["company"],
            "gender": user_info["gender"],
            "position": user_info["position"],
        }
        return user_dict
