from flask import Blueprint
from flask_restful import Api

from lawyer.resources.users import passport

# 创建蓝图对象
user_blue = Blueprint("user", __name__)

# 关联蓝图
user_api = Api(user_blue, catch_all_404s=True)

# 添加路由资源到对象中
# 注册
user_api.add_resource(passport.NewClientResource, "/v1_0/new_client", endpoint="NewClient")
# 发送验证码
user_api.add_resource(passport.SMSCodeResource, "/v1_0/sms_code/<path:mobile>", endpoint="SMSCode")
# 登陆
user_api.add_resource(passport.AuthorizationResouce, "/v1_0/authorizations", endpoint="AuthorizationResouce")
