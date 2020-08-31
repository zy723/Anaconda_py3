from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.models.city import City


class ProvinceResource(Resource):
    """
    省市区 三级联动
    获取省份
    """

    def get(self):
        # 查询所有的省份信息
        cities = City.query.filter(City.parent_id == None).all()
        # 拼接返回数据
        data_list = []
        for item in cities:
            data_list.append({
                "province_id": item.id,
                "province_name": item.name
            })
        return data_list


class CityResource(Resource):
    """
    获取城市信息
    """

    def get(self):
        # 解析参数
        rp = RequestParser()
        rp.add_argument("pid", type=int, required=True, location="args")

        # 获取参数
        args = rp.parse_args()
        pid = args.get("pid")

        # 查询城市信息
        citys = City.query.filter(City.parent_id == pid).all()

        city_list = []
        for city in citys:
            city_list.append({
                "city_id": city.id,
                "city_name": city.name
            })
        return city_list


class DistrictResource(Resource):
    """
    获取区域信息
    """

    def get(self):
        # 解析参数
        rp = RequestParser()
        rp.add_argument("pid", type=int, required=True, location="args")

        # 获取参数
        args = rp.parse_args()
        pid = args.get("pid")

        # 查询区域信息
        districts = City.query.filter(City.parent_id == pid).all()

        city_list = []
        for city in districts:
            city_list.append({
                "city_id": city.id,
                "city_name": city.name
            })
        return city_list
