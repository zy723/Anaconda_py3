from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.utils import parser


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
