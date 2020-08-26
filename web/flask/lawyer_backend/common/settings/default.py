import logging


class DefaultConfig(object):
    # 配置密钥
    SECRET_KEY = "AAAAAAAAAAAAA"
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://dbmysql:dbmysql@127.0.0.1/lawyer_ol"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 数据库主从配置
    # SLAVE_HOST = "172.16.12.134"
    # SLAVE_PORT = 8306
    # SLAVE_USER = "root"
    # SLAVE_PASSWORD = "mysql"
    # SLAVE_DATABASE = "lawyer_ol"
    # SLAVE_CHARSET = "utf8"

    # 默认日志级别
    LOG_LV = logging.DEBUG

    # redis集群
    REDIS_CLUSTER = [
        {"host": "127.0.0.1", "port": "6379"},
        # {"host": "192.168.0.114", "port": "6381"},
    ]

    # redis主从
    REDIS_SENTINELS = [
        ("127.0.0.1", "6379"),
    ]
    REDIS_SENTINEL_SERVICES_NAME = "mymaster"


class DevelopConfig(DefaultConfig):
    """
    开发模式配置
    """
    DEBUG = True


class ProductConfig(DefaultConfig):
    """
    生成模式配置
    """
    DEBUG = False
    LOG_LV = logging.ERROR


# 设置入口访问字典
config_dict = {
    "development": DevelopConfig,
    "production": ProductConfig
}
