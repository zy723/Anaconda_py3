from common.cache.constants import DataTTLBase


class BasicCache(object):

    def __init__(self):
        self.TTL_cache = DataTTLBase.get_value()

    def get(self):
        pass
        # TODO 添加缓存




