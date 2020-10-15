import random


class DataTTLBase(object):
    TTL = 60 * 60 * 2
    MAX_DELTA = 60 * 10

    @classmethod
    def get_value(cls):
        return cls.TTL + random.randint(0, cls.MAX_DELTA)


class UserCacheDataTTL(DataTTLBase):
    pass


class UserNotExistsTTL(DataTTLBase):
    TTL = 60 * 5
    MAX_DELTA = 60 * 1


class QustCacheDataTTL(DataTTLBase):
    pass


class QustNotExistsTTL(DataTTLBase):
    TTL = 60 * 5
    MAX_DELTA = 60 * 1


class LawyerCacheDataTTL(DataTTLBase):
    TTL = 60 * 60 * 1
    MAX_DELTA = 60 * 8


class LawyerNotExistsTTL(DataTTLBase):
    TTL = 60 * 4
    MAX_DELTA = 60 * 1


class UserIdCacheDataTTL(DataTTLBase):
    TTL = 60 * 60 * 4
    MAX_DELTA = 60 * 10


class UserIdNotExistsTTL(DataTTLBase):
    TTL = 60 * 4
    MAX_DELTA = 60 * 1


class UserSearchingHistoryCacheDataTTL(DataTTLBase):
    TTL = 60 * 60 * 24 * 30
    MAX_DELTA = 60 * 50


class UserSearchingHistoryNotExistsTTL(DataTTLBase):
    TTL = 60 * 60 * 5
    MAX_DELTA = 60 * 1
