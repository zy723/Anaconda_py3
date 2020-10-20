from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.cache.lawyer import LawyerCache
from common.utils.slave_db_router import Queries


class LawyersResource(Resource):
    def get(self):
        # 获取参数
        rp = RequestParser()
        rp.add_argument("by", type=str, required=True, location="args")
        rp.add_argument("p", type=str, required=True, location="args")
        # 解析参数
        args = rp.parse_args()
        by = args.by
        p = args.p
        # 判断参数的类型(地区, 专业， 评分)， 查询数据
        lawyer_ids = None
        if by == "1":  # 地区
            sql = """select user_id from user_basic where city_id=%s;"""
            lawyer_ids = Queries.fetchall(sql, [p])
        elif by == "2":  # 专业
            sql = """select lawyer_id from lawyer_expertise where expertise_id=%s;"""
            lawyer_ids = Queries.fetchall(sql, [p])
        elif by == "3":  # 评分
            # select lawyer_id from lawyer_basic where l_score between %s and %s;
            sql = """select lawyer_id from lawyer_basic where l_score between %s and %s;"""
            lst = [[0, 5], [4, 5], [3, 4], [2, 3], [0, 2]]
            lawyer_ids = Queries.fetchall(sql, lst[int(p) - 1])

        # 取出数据， 拼接数据
        lawyer_list = []
        for lawyer_id in lawyer_ids:
            lawyer_dict = LawyerCache(lawyer_id[0]).get()
            lawyer_list.append(lawyer_dict)

        return lawyer_list


class HotLowersResource(Resource):
    """
    获取热门律师列表
    """

    def get(self):
        # 根据评分查询律师信息
        sql = """select lawyer_id from lawyer_basic order by l_score limit 5"""
        data = Queries.fetchall(sql, [])

        # 拼接参数
        lawyer_list = []
        for item in data:
            lawyer_list.append(LawyerCache(item[0]).get())

        # 返回数据
        return {
            "lawyer_list": lawyer_list,
            "message": "success",
            "status": 200
        }
