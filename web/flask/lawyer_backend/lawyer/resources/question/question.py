from flask_restful import Resource
from flask_restful.reqparse import RequestParser

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
            # TODO 01 cache
            pass

        return dataList
