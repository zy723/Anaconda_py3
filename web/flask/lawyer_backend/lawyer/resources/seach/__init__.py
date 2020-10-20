from flask import Blueprint
from flask_restful import Api

from lawyer.resources.seach import search

# 1 创建蓝图
search_blue = Blueprint("search", __name__)
search_api = Api(search_blue, catch_all_404s=True)
# 2. 添加类视图

# 搜索类视图
search_api.add_resource(search.HistoryDataResource, "/v1_0/search/histories", endpoint="HistoryDataResource")
search_api.add_resource(search.SuggestionResource, "/v1_0/search/suggestion", endpoint="SuggestionResource")
search_api.add_resource(search.SearchResource, "/v1_0/search/search", endpoint="SearchResource")
