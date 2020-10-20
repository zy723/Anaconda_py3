from common.cache.base_cache import BasicCache
from common.cache.constants import LawyerCacheDataTTL, LawyerNotExistsTTL
from common.models.user import Lawyer, User


class LawyerCache(BasicCache):
    """
    获取律师的字典数据
    """

    def __init__(self, id):
        """
        初始化
        :param id:
        """
        self.id = id
        self.key = "lawyer:{}".format(self.id)
        self.TTL_Cache = LawyerCacheDataTTL.get_value()
        self.TTL_Not_Exists = LawyerNotExistsTTL.get_value()

    def get_data_obj(self):
        # 获取律师对象
        lawyer = Lawyer.query.get(self.id)
        if not lawyer:
            return None
        return lawyer

    def create_obj_dict(self, lawyer):
        expertise_list = []
        for expertise in lawyer.expertises:
            expertise_list.append(expertise.name)

        # 将对象转换成字典数据
        lawyer_dict = {
            "practice_year": lawyer.practice_year,
            "id": lawyer.id,
            "paid_for_hour": lawyer.paid_for_hour,
            "l_score": int(lawyer.l_score),
            "real_name": lawyer.real_name,
            "is_certified": lawyer.is_certified,
            "paid_for_once": lawyer.paid_for_once,
            "expertise": expertise_list,
            "is_following": False,
            "profile_photo": User.query.get(self.id).profile_photo,
            "lawyer_firm": lawyer.lawyer_firm
        }
        # 返回数据
        return lawyer_dict
