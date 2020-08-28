
from flask import Blueprint
from flask_restful import Api

from lawyer.resources.question import question

question_bp = Blueprint("question", __name__)

question_api = Api(question_bp, catch_all_404s=True)

# 首页问题获取
question_api.add_resource(question.NewQuesionResource, "/v1_0/new_question", endpoint="NewQuesionResource")
