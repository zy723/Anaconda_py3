import logging

from flask import current_app

from common.models.user import User
from common.utils.slave_db_router import DBOpenExe, Queries
from common.utils.snowflake.id_worker import IdWorker
from lawyer import create_app

app = create_app()


@app.route('/')
def hello_word():
    print(app.url_map)
    # 测试数据库
    # print(User.query.all())
    # 测试从数据库
    # sql = """select * from user_basic where mobile=%s;"""
    # cmd = ["13300000002", ]
    # with DBOpenExe(sql, cmd) as cs:
    #     data = cs.fetchall()
    # data = Queries.fetchall(sql, cmd)
    # print(data)

    # 测试logger
    # logging.debug(User.query.all())
    # logging.error("error test")
    # 集群测试
    # 已修改为单redis
    # current_app.redis_cluster.set("name", "helloword")
    # print(current_app.redis_cluster.get("name"))

    # 测试雪花算法
    # worker = IdWorker(1, 2, 0)
    # print(worker.get_id())

    return "hello word", 400


if __name__ == '__main__':
    app.run(debug=True)
