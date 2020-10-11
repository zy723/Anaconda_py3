from common.models.city import City
from common.models.user import User


class UserCache(object):
    """
    根据用户对象获取用户ID
    """
    def __init__(self, id):
        self.id = id

    def get(self):
        # 根据用户对象查询
        user = User.query.filter(User.id == self.id).first()
        # 判断用户对象是否存在
        if not user:
            return None
        # 将用户对象转换成字典
        city_name = None
        if user.city:
            city = City.query.get(user.city)
            if city:
                city_name = city.name

        user_dict = {
            "mobile": user.mobile,
            "company": user.company,
            "gender": user.gender,
            "position": user.position,
            "profile_photo": user.profile_photo,
            "city_name": city_name,
            "name": user.name,
        }

        return user_dict
