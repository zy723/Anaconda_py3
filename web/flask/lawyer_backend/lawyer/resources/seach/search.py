from flask_restful import Resource

from common.utils.login_required import login_required


class HistoryDataResource(Resource):
    """
    搜索历史记录
    """

    method_decorators = {
        "get": [login_required]
    }

    def get(self):
        pass
