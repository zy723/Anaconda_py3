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
