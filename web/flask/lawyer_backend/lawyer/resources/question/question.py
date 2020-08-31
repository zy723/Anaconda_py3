import werkzeug
from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.cache.question import QuestionBasicCache
from common.models import db
from common.models.question_answer import Question, QuestionContent
from common.utils import parser
from common.utils.image_storage import image_storage
from common.utils.slave_db_router import Queries


class NewQuesionResource(Resource):
    """
    首页问题获取
    """

    def get(self):
        # 解析参数
        rp = RequestParser()
        rp.add_argument("cur_page", type=int, required=True, location="args")
        rp.add_argument("per_page_count", type=int, required=True, location="args")

        # 获取参数
        args = rp.parse_args()
        cur_page = args.cur_page
        per_page_count = args.per_page_count

        # 查询法律问题
        sql = """select * from question_basic order by update_time desc limit %s,%s;"""
        data = Queries.fetchall(sql, [(cur_page - 1) * per_page_count, per_page_count])

        # 封装数据并返回
        dataList = []
        for item in data:
            question = QuestionBasicCache(item[0]).get()
            dataList.append({
                "id": question["id"],
                "title": question["title"],
                "author_name": question["author_name"],
                "expertise": question["expertise"],
                "city": question["city"],
                "create_time": question["create_time"],
                "answer_count": 0,
            })

        return dataList


class QuesionResource(Resource):
    """
    提交问题
    """

    def post(self):
        # 解析参数
        rp = RequestParser()
        rp.add_argument("title", type=str, location="form")
        rp.add_argument("content", type=str, location="form")
        rp.add_argument("city_id", type=int, location="form")
        rp.add_argument("expertise_id", type=int, location="form")
        rp.add_argument("p0", type=parser.image_file, location="files")
        rp.add_argument("p1", type=parser.image_file, location="files")
        rp.add_argument("p2", type=parser.image_file, location="files")
        # 获取参数
        args = rp.parse_args()
        title = args.title
        content = args.content
        city_id = args.city_id
        expertise_id = args.expertise_id
        p0 = args.p0
        p1 = args.p1
        p2 = args.p2
        # 存入数据库
        try:
            question = Question()
            question.user_id = 1191875991891345408
            question.city_id = city_id
            question.expertise_id = expertise_id
            question.title = title
            db.session.add(question)
            db.session.flush()

            question_content = QuestionContent(id=question.id, content=content)
            db.session.add(question_content)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return {"message": "问题发布失败"}, 500

        # 上传图片
        image_list = []
        for item in [p0, p1, p2]:
            if item:
                image_name = image_storage(item.read())
                image_url = "http://qfxw7xaut.hn-bkt.clouddn.com/" + image_name
                image_list.append(image_url)

        # 数据存于数据库中
        try:
            Question.query.filter(Question.id == question.id).update({"cover": image_list})
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return {"message": "图片存储失败", "code": 0}, 500

        # 返回响应
        return {"message": "ok", "code": 1, "forent_images": image_list}
