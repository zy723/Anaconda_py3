from flask import g, current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.cache.user import UserCache
from common.models import db
from common.models.user import User
from common.utils.image_storage import image_storage
from common.utils.login_required import login_required
from common.utils.parser import image_file


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
            "user_photo_url": current_app.config["QINIU_DOMAIN"] + user_info["profile_photo"],
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


class UserPhotoResource(Resource):
    """
    用户头像上传
    """
    method_decorators = {
        "post": [login_required]
    }

    def post(self):
        rp = RequestParser()
        rp.add_argument("photo", type=image_file, location="files")
        args = rp.parse_args()
        photo = args.photo

        # 上传头像
        image_name = image_storage(photo.read())
        if not image_name:
            return {"message": "files update failed"}, 400

        if image_name:
            try:
                User.query.filter(User.id == g.user_id).update({"profile_photo": image_name})
                db.session.commit()
            except Exception as e:
                current_app.logger.error(e)
                return {"message": "files save failed"}, 400

        photo_url = current_app.config["QINIU_DOMAIN"] + image_name
        return {
            "photo_url": photo_url
        }
