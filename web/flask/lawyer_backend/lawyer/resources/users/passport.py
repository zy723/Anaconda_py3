import logging
import random
from datetime import datetime

from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.models import db
from common.models.user import User, Lawyer
from common.utils import parser
from common.utils.jwt_utils import generate_token
from common.utils.parser import mobile
from common.utils.slave_db_router import Queries
from common.utils.yuntongxun.sms import CCP


class AuthorBasic(object):

    def _generate_token(self, user_id, role):
        """
        生成Token
        :param user_id:
        :param role:
        :return:
        """
        token = generate_token(user_id, role, current_app.config.get("TOKEN_HOURS"))
        self._save_token(user_id, token)
        return token

    def _save_token(self, user_id, token):
        key = "token:{}".format(user_id)
        current_app.redis_master.setex(key, current_app.config.get("TOKEN_HOURS"), token)


class NewClientResource(Resource, AuthorBasic):
    """
    注册类视图
    """

    def post(self):
        rp = RequestParser()
        rp.add_argument("mobile", type=parser.mobile, required=True, location="json")
        rp.add_argument("password", type=parser.regex(r"^\w{6,12}$"), required=True, location="json")
        rp.add_argument("code", type=parser.regex(r"^\d{6}$"), required=True, location="json")
        rp.add_argument("expert_ident", type=parser.regex(r"^\d{17}$"), location="json")

        # 获取参数
        args = rp.parse_args()
        mobile = args.mobile
        password = args.password
        code = args.code
        expert_ident = args.expert_ident

        # 校验验证码/判断用户是否存在
        sql = """select mobile from user_basic where mobile=%s"""
        user = Queries.fetchone(sql, [mobile, ])
        if user:
            return {"message": "user already exists"}, 400
        try:
            send_code = current_app.redis_master.get("SMS_CODE:{}".format(mobile))
        except Exception as e:
            send_code = None
            current_app.logger.error(e)
            # send_code = current_app.redis_slave.get("SMS_CODE:{}".format(mobile))
        if send_code is None or send_code.decode() != code:
            return {"message": "sms code error"}, 400

        # 不存在 存储用户
        # 生成用户id 雪花算法
        user_id = current_app.id_worker.get_id()
        user = User(id=user_id, mobile=mobile, name=mobile, last_login=datetime.now(), ctime=datetime.now(),
                    password=password)
        db.session.add(user)
        # 是否是律师  如果是存储
        if expert_ident:
            user.role = 2
            lawyer = Lawyer(id=user.id)
            lawyer.expert_ident = expert_ident
            lawyer.real_name = user.name
            db.session.add(lawyer)

        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return {"massage": "add user fail"}, 502

        # 清除缓存

        # 生成token
        token = self._generate_token(user_id, user.role)
        # 返回状态

        return {"code": 0, "msg": "ok", "token": token}


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


class AuthorizationResouce(Resource, AuthorBasic):
    """
    登陆
    """

    def post(self):
        # 解析参数
        rp = RequestParser()
        rp.add_argument("mobile", type=parser.mobile, required=True, location="json")
        rp.add_argument("password", type=parser.regex(r"^\w{5,12}$"), required=True, location="json")

        # 获取参数
        args = rp.parse_args()
        mobile = args.get("mobile")
        password = args.get("password")

        # 判断用户是否存在
        user = User.query.filter(User.mobile == mobile).first()
        if not user:
            return {"massage": "user is not exists"}, 400
        # 校验密码
        if not user.check_password(password):
            return {"massage": "authorization faild"}, 400

        token = self._generate_token(user.id, user.role)
        return {"code": 0, "msg": "ok", "token": token}
