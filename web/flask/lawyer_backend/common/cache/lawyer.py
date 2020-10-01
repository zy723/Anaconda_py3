from common.models.user import Lawyer, User


class LawyerCache(object):
    """
    获取律师的字典数据
    """

    def __init__(self, id):
        """
        初始化
        :param id:
        """
        self.id = id

    def get(self):
        """
        获取用户字典数据
        :return:
        """
        # 获取律师对象
        lawyer = Lawyer.query.get(self.id)
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
            "expertises": expertise_list,
            "is_following": False,
            "profile_photo": User.query.get(self.id).profile_photo,
            "lawyer_firm": lawyer.lawyer_firm
        }
        # 返回数据
        return lawyer_dict
