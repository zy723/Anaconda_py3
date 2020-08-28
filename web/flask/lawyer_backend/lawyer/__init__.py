from flask import Flask
from flask_cors import CORS
from redis.sentinel import Sentinel
from rediscluster import RedisCluster

from common.settings.default import config_dict
from common.utils.logger import log_file
from common.utils.snowflake.id_worker import IdWorker


def create_app():
    # 工厂模式
    # 创建app对象
    app = Flask(__name__)

    # 设置跨域访问
    CORS(app)

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
    import redis
    app.redis_cluster = redis.StrictRedis(host=app.config.get("REDIS_CLUSTER")[0]['host'],
                                          port=app.config.get("REDIS_CLUSTER")[0]['port'], db=0)

    # redis 哨兵 主从配置
    # sentinel = Sentinel(app.config.get("REDIS_SENTINELS"))
    # app.redis_master = sentinel.master_for(app.config.get("REDIS_SENTINEL_SERVICES_NAME"))
    # app.redis_slave = sentinel.slave_for(app.config.get("REDIS_SENTINEL_SERVICES_NAME"))
    app.redis_master = app.redis_cluster
    app.redis_slave = app.redis_cluster

    # 雪花算法生成用户ID
    app.id_worker = IdWorker(app.config["DATACENTER_ID"],
                             app.config["WORKER_ID"],
                             app.config["SEQUENCE"])

    # 注册蓝图对象到app中

    from .resources.users import user_blue
    app.register_blueprint(user_blue)

    from .resources.question import question_bp
    app.register_blueprint(question_bp)
    return app
