import random

from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.utils import parser
from common.utils.parser import mobile
from common.utils.slave_db_router import Queries
from common.utils.yuntongxun.sms import CCP


class NewClientResource(Resource):
    """
    注册类视图
    """

    def get(self):
        return {"name": "xf"}

    def post(self):
        rp = RequestParser()
        rp.add_argument("mobile", type=parser.mobile, required=True, location="json")
        rp.add_argument("password", type=parser.regex(r"^\w{6,12}$"), required=True, location="json")
        rp.add_argument("code", type=parser.regex(r"^\d{6}$"), required=True, location="json")
        rp.add_argument("expert_ident", type=parser.regex(r"^\d{17}$"), location="json")

        # 获取参数
        args = rp.parse_args()
        password = args.password
        code = args.code
        expert_ident = args.expert_ident

        return {"code": 0, "msg": "ok"}


class AuthorizationResource(Resource):
    pass


class SMSCodeResource(Resource):
    """
    发送手机验证码
    """

    def get(self, mobile):
        # 验证手机号是否存在
        sql = """select mobile from user_basic where mobile=%s;"""
        user = Queries.fetchone(sql, [mobile, ])
        if user:
            return {"message": "user is already exists"}, 400

        # 不存在发送验证码
        sms_code = "%06d" % random.randint(0, 999999)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)

        # 存储临时验证码到redis中
        current_app.redis_master.setex("SMS_CODE:{}".format(mobile), 60 * 5, sms_code)
        # 返回相应
        return {"mobile": mobile, "code": sms_code}
