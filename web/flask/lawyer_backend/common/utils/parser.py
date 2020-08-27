import re
import imghdr


def mobile(mobile_str):
    """
    手机校验格式
    """
    if re.match(r'^1[3-9]\d{9}$', mobile_str):
        return mobile_str
    else:
        raise ValueError("{} is not valid mobile".format(mobile_str))


def regex(pattern):
    """
    校验正则表达式内容
    """

    def validate(value_str):
        if re.match(pattern, value_str):
            return value_str
        else:
            raise ValueError("invalid params")

    return validate


def image_file(value):
    """
    校验图片
    """
    try:
        file_type = imghdr.what(value)
    except Exception:
        raise ValueError("invalid image")

    if file_type:
        return value
    else:
        raise ValueError("invalid image")
