import json

from flask import current_app
from redis import RedisError

from common.cache.constants import DataTTLBase, UserNotExistsTTL


class BasicCache(object):

    def __init__(self):
        self.key = None
        self.TTL_Cache = DataTTLBase.get_value()
        self.TTL_Not_Exists = UserNotExistsTTL.get_value()

    def get_data_obj(self):
        return None

    def create_obj_dict(self, obj):
        return None

    def get(self):
        # 1. 从redis 中获取查看是否有缓存
        redis_cluster = current_app.redis_cluster

        try:
            redis_data = redis_cluster.get(self.key)
        except Exception as e:
            current_app.logger.error(e)
            redis_data = None

        # redis_data = None
        # 2. 判断数据是否存在
        if redis_data:
            return json.loads(redis_data)
        # 2.1 解决缓存穿透bug
        if redis_data == "-1":
            return None

        # 3. 获取对象数据
        obj = self.get_data_obj()

        if not obj:
            return None

        # 4. 对象转换成字典
        obj_dict = self.create_obj_dict(obj)

        # 判断缓存数据是否存在
        if obj_dict:
            try:
                redis_cluster.setex(self.key, self.TTL_Cache, json.dumps(obj_dict))
            except Exception as e:
                current_app.logger.error(e)
        else:
            try:
                redis_cluster.setex(self.key, self.TTL_Not_Exists, "-1")
            except Exception as e:
                current_app.logger.error(e)

        return obj_dict

    def clear(self):
        """
        手动清除缓存
        :return:
        """

        try:
            redis_cluster = current_app.redis_cluster
            redis_cluster.delete(self.key)
        except RedisError as e:
            current_app.logger.error(e)

    def exists(self):
        """
        判断数据是否存在
        :return:
        """
        ret = self.get()
        if ret:
            return True
        else:
            return False
