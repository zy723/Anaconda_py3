from sqlalchemy.orm import load_only

from common.cache.base_cache import BasicCache
from common.models.city import City
from common.models.question_answer import Question
from common.models.user import User
from lawyer.resources.question.expertise import EXPERTISE


class QuestionBasicCache(object):
    """
    获取question对象,缓存类
    """

    def __init__(self, id):
        self.id = id

    def get(self):
        """
        获取对象
        :return:
        """
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

        obj_dict = {
            "id": obj.id,
            "title": obj.title,
            "author_name": User.query.filter(User.id == obj.user_id).first().name,
            "expertise": EXPERTISE[obj.expertise_id - 1][1] if obj.expertise_id else None,
            "city": City.query.filter_by(id=obj.city_id).first().name if City.query.filter_by(
                id=obj.city_id).first() is not None else "",
            "create_time": obj.ctime.strftime("%Y-%m-%d %H:%M:%S")
        }
        return obj_dict
