import json

from flask import current_app

from common.cache.constants import DataTTLBase


class BasicCache(object):

    def __init__(self):
        self.TTL_Cache = DataTTLBase.get_value()

    def get(self):
        # 1. 从redis 中获取查看是否有缓存
        redis_cluster = current_app.redis_cluster

        try:
            redis_data = redis_cluster.get(self.key)
        except Exception as e:
            current_app.logger.error(e)
            redis_data = None

        # 2. 判断数据是否存在
        if redis_data:
            return json.loads(redis_data)
        # 3. 获取对象数据
        obj = self.get_data_obj()
        # 4. 对象转换成字典
        obj_dict = self.create_obj_dict(obj)
        redis_cluster.setex(self.key, self.TTL_Cache, json.dumps(obj_dict))

        return obj_dict
