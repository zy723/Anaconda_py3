from flask import Blueprint
from flask_restful import Api

# 1.创建蓝图对象
from lawyer.resources.consult import consult

consult_blue = Blueprint("consult", __name__)

consult_api = Api(consult_blue)

# 2.添加资源到Api对象中
consult_api.add_resource(consult.LawyersResource, "/v1_0/lawyers", endpoint="LawyersResource")
