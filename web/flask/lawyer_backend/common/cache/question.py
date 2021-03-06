import json

from flask import g
from sqlalchemy.orm import load_only

from common.cache.base_cache import BasicCache
from common.cache.constants import QustCacheDataTTL, QustNotExistsTTL
from common.models.city import City
from common.models.question_answer import Question, QuestionContent, Answer
from common.models.user import User, Lawyer, Relation
from lawyer.resources.question.expertise import EXPERTISE


class QuestionBasicCache(BasicCache):
    """
    获取question对象,缓存类
    """

    def __init__(self, _id):
        self.id = _id
        self.key = "question_base:{}".format(self.id)
        self.TTL_Cache = QustCacheDataTTL.get_value()
        self.TTL_Not_Exists = QustNotExistsTTL.get_value()

    def get_data_obj(self):
        obj = Question.query.options(
            load_only(
                Question.id,
                Question.title,
                Question.user_id,
                Question.expertise_id,
                Question.city_id,
                Question.ctime
            )
        ).filter_by(id=self.id).first()
        if not obj:
            return None
        return obj

    def create_obj_dict(self, obj):
        city = City.query.filter_by(id=obj.city_id).first()
        author = User.query.filter(User.id == obj.user_id).first()

        obj_dict = {
            "id": obj.id,
            "title": obj.title,
            "author_name": author.name,
            "expertise": EXPERTISE[obj.expertise_id - 1][1] if obj.expertise_id else None,
            "city": city.name if city else None,
            "create_time": obj.ctime.strftime("%Y-%m-%d %H:%M%S"),
            "user_id": author.id
        }
        return obj_dict


class QuestionContentCache(BasicCache):
    """
    根据用户ID 获取问题内容
    """

    def __init__(self, id):
        self.id = id
        self.key = "question_content:{}".format(self.id)
        self.TTL_Cache = QustCacheDataTTL.get_value()
        self.TTL_Not_Exists = QustNotExistsTTL.get_value()

    def get_data_obj(self):
        content = QuestionContent.query.get(self.id)
        if not content:
            return None
        return content

    def create_obj_dict(self, obj):
        content_dict = {
            "id": obj.id,
            "content": obj.content
        }

        return content_dict


class AnswerCache(BasicCache):
    """
    获取问题 回答列表
    """

    def __init__(self, _id):
        self.id = _id
        self.key = "answer:{}".format(self.id)
        self.TTL_Cache = QustCacheDataTTL.get_value()
        self.TTL_Not_Exists = QustNotExistsTTL.get_value()

    def get_data_obj(self):
        answers = Answer.query.options(
            load_only(Answer.id, Answer.qust_id, Answer.content, Answer.status, Answer.ctime, )).filter(
            Answer.qust_id == self.id).all()

        if not answers:
            return None

        return answers

    def create_obj_dict(self, answers):

        answer_list = []

        for answer in answers:
            user = User.query.get(answer.lawyer_id)
            lawyer = Lawyer.query.get(answer.lawyer_id)
            # 查询用户与律师关系
            relation = Relation.is_following(user_id=g.user_id, lawyer_id=lawyer.id)
            is_following = 0
            if relation:
                is_following = 1
            answer_dict = {
                "ans_name": user.name,
                "ans_photo_url": user.profile_photo,
                "create_time": answer.ctime.strftime("%Y-%m-%d %H-%M-%S"),
                "content": answer.content,
                "lawyer_id": answer.lawyer_id,
                "is_following": is_following,
                "paid_for_once": lawyer.paid_for_once,
                "paid_for_hour": lawyer.paid_for_hour,
            }
            answer_list.append(answer_dict)

        return answer_list
