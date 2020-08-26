import logging

from flask import current_app

from common.models.user import User
from lawyer import create_app

app = create_app()


@app.route('/')
def hello_word():
    # 测试数据库
    print(User.query.all())
    # 测试logger
    # logging.debug(User.query.all())
    logging.error("error test")
    # 集群测试
    # TODO 待修改bug
    # current_app.redis_cluster.set("name", "helloword")
    # print(current_app.redis_cluster.get("name"))


    return "hello word", 400


if __name__ == '__main__':
    app.run(debug=True)
