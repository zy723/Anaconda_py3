from flask import Flask
from redis.sentinel import Sentinel
from rediscluster import RedisCluster

from common.settings.default import config_dict
from common.utils.logger import log_file


def create_app():
    # 工厂模式
    # 创建app对象
    app = Flask(__name__)

    # 加载配置信息
    config = config_dict.get(app.config.get('ENV'))
    app.config.from_object(config)

    # 配置数据库
    from common.models import db
    db.init_app(app)

    # 记录日志信息
    log_file(app, config.LOG_LV)

    # TODO 待修改bug 01
    # redis 集群加载
    # app.redis_cluster = RedisCluster(startup_nodes=app.config.get("REDIS_CLUSTER"), decode_responses=True)

    # redis 哨兵 主从配置
    # sentinel = Sentinel(app.config.get("REDIS_SENTINELS"))
    # app.redis_master = sentinel.master_for(app.config.get("REDIS_SENTINEL_SERVICES_NAME"))
    # app.redis_slave = sentinel.slave_for(app.config.get("REDIS_SENTINEL_SERVICES_NAME"))

    # 注册蓝图对象到app中
    from .resources.users import user_blue
    app.register_blueprint(user_blue)
    return app
