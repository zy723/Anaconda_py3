from flask import g, current_app
from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser

from common.cache.search import UserSearchingHistoryCache
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
