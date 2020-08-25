from flask import current_app
from pymysql import connect


class DBOpenExe(object):
    """
    上下文管理器 配合with使用
    """

    def __init__(self):
        self.conn = connect(
            host=current_app.config.get("SLAVE_HOST"),
            port=current_app.config.get("SLAVE_PORT"),
            user=current_app.config.get("SLAVE_USER"),
            password=current_app.config.get("SLAVE_PASSWORD"),
            database=current_app.config.get("SLAVE_DATABASE"),
            charset=current_app.config.get("SLAVE_CHARSET"),
        )
        self.cs = self.conn.cursor()

    def __enter__(self):
        """
        创建连接之前调用
        :return:
        """
        return self.cs

    def __exit__(self, *args):
        """
        连接完成调用
        :param args:
        :return:
        """
        self.conn.commit()
        self.cs.close()
        self.conn.close()
