from flask import g, current_app
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser

from common.cache.question import QuestionBasicCache
from common.cache.search import UserSearchingHistoryCache
from common.cache.user import UserCache
from common.utils.login_required import login_required


class HistoryDataResource(Resource):
    """
    搜索历史记录
    """

    method_decorators = {
        "get": [login_required]
    }

    def get(self):
        ret = UserSearchingHistoryCache(g.user_id).get()
        if not ret:
            ret = {
                "history_searching_list": []
            }

        return ret


class SuggestionResource(Resource):
    """
    搜索字符串
    """

    def get(self):
        # 1. 获取参数并解析
        rp = RequestParser()
        rp.add_argument("k", type=inputs.regex(r'^.{1,50}$'), required=True, location="args")
        args = rp.parse_args()
        key = args.get('k')
        # 2. 查询数据
        query = {
            "from": 0,
            "size": 10,
            "_source": False,
            "suggest": {
                "word-completion": {
                    "prefix": key,
                    "completion": {
                        "field": "suggest"
                    }
                }
            }
        }

        ret = current_app.es.search(index="completions", body=query)
        # 3. 拼接数据
        options = ret["suggest"]["word-completion"][0]["options"]
        data_list = []
        for option in options:
            data_list.append(option["text"])
        # 4. 反馈数据
        return data_list


class SearchResource(Resource):
    """
    根据关键字搜索内容
    """

    def get(self):
        # 1. 获取参数 解析参数
        rp = RequestParser()
        rp.add_argument("k", type=str, required=True, location="args")
        rp.add_argument("cur_page", type=int, required=True, location="args")  # 页码数
        rp.add_argument("per_page_count", type=int, required=True, location="args")  # 每页显示数量

        args = rp.parse_args()

        key = args.k
        cur_page = args.cur_page
        per_page_count = args.per_page_count
        # 2. 查询数据
        query = {
            "from": (cur_page - 1) * per_page_count,
            "size": per_page_count,
            "query": {
                "bool": {
                    "must": [{"match": {"_all": key}}],
                    "filter": [{"term": {"status": "2"}}]
                }
            }

        }
        ret = current_app.es.search(index="qusts", doc_type="qust", body=query)
        # 3. 拼接数据
        hists_list = ret["hits"]["hits"]
        id_list = []
        data_list = []
        for hit in hists_list:
            id_list.append(hit["_id"])

        for item in id_list:
            question = QuestionBasicCache(item).get()
            user = UserCache(question["user_id"]).get()
            data_dict = {
                "city": question["city"],
                "create_time": question["create_time"],
                "answer_count": 0,
                "id": question["id"],
                "author_name": user["name"],
                "title": question["title"],
                "expertise": question["expertise"],
                "author_photo_url": user["profile_photo"],
            }
            data_list.append(data_dict)

        # 添加搜索历史记录
        if g.user_id:
            current_app.logger.error(g.user_id)
            user_h = UserSearchingHistoryCache(g.user_id)
            user_h.save(key)

        # 4. 返回数据

        return data_list
