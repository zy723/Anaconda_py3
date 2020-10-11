
from flask import Blueprint
from flask_restful import Api

from lawyer.resources.question import question

question_bp = Blueprint("question", __name__)

question_api = Api(question_bp, catch_all_404s=True)

# 首页问题获取
question_api.add_resource(question.NewQuesionResource, "/v1_0/new_questions", endpoint="NewQuesionResource")
# 提交问题
question_api.add_resource(question.QuesionResource, "/v1_0/question", endpoint="QuesionResource")
# 问题详情
# question_api.add_resource(question.QuesionDetailResource, "/v1_0/question", endpoint="QuesionDetailResource")
