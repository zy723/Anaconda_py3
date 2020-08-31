from flask import Blueprint
from flask_restful import Api

from lawyer.resources.common import common

common_bp = Blueprint("common", __name__)
common_api = Api(common_bp, catch_all_404s=True)

# 加载类视图
# 获取省份
common_api.add_resource(common.ProvinceResource, "/v1_0/common/provinces", endpoint="ProvinceResource")
# 获取城市信息
common_api.add_resource(common.CityResource, "/v1_0/common/city", endpoint="CityResource")
# 获取区域信息
common_api.add_resource(common.DistrictResource, "/v1_0/common/districts", endpoint="DistrictResource")
