import random


class DataTTLBase(object):
    TTL = 60 * 60 * 2
    MAX_DELTA = 60 * 10

    @classmethod
    def get_value(cls):
        return cls.TTL + random.randint(0, cls.MAX_DELTA)
