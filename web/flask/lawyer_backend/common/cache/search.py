import json

from flask import current_app

from common.cache.base_cache import BasicCache
from common.cache.constants import UserSearchingHistoryCacheDataTTL, UserSearchingHistoryNotExistsTTL


class UserSearchingHistoryCache(BasicCache):

    def __init__(self, _id):
        self.id = _id
        self.key = "user:{}:history:searching".format(id)
        self.TTL_Cache = UserSearchingHistoryCacheDataTTL.get_value()
        self.TTL_Not_Exists = UserSearchingHistoryNotExistsTTL.get_value()

    def get_data_obj(self):
        objs = None
        return objs

    def create_obj_dict(self, obj):
        return None

    def save(self, words):
        """
        保持缓存记录
        """
        # 获取历史信息
        ret = self.get()
        # 判断历史信息是否已经存在
        if ret is None:
            obj_dict = {"history_searching_list": []}
        else:
            obj_dict = ret

        # 不存在 添加记录到redis中
        if words not in obj_dict["history_searching_list"]:
            obj_dict["history_searching_list"].append(words)
        # 设置数据到redis中

        redis_cluster = current_app.redis_cluster
        redis_cluster.setex(self.key, self.TTL_Cache, json.dumps(obj_dict))
