import logging
import os
from logging.handlers import RotatingFileHandler


def log_file(app, log_lv):
    """
    记录日志信息
    :param app:
    :param log_lv:
    :return:
    """
    filename = os.path.join(os.path.dirname(app.instance_path), 'logs', 'log')
    # 设置哪些日志信息等级要被记录
    logging.basicConfig(level=log_lv)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler(filename, maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter("%(levelname)s %(filename)s:%(lineno)d %(message)s")
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
