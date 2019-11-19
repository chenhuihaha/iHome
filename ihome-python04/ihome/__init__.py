"""
@Time    : 2019/11/8 下午7:42
@Author  : chenhui
@FileName: __init__.py.py
@Software: PyCharm
"""
from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from ihome import api_1_0
import pymysql
import logging
from logging.handlers import RotatingFileHandler

pymysql.install_as_MySQLdb()

import redis

# 数据库
db = SQLAlchemy()

# 创建redis连接对象
redis_store = None

# 为flask补充csrf的防护机制
csrf = CSRFProtect()

# 打印的信息写到日志文件中
logging.error('')  # 错误级别
logging.warn('')  # 警告级别
logging.info('')  # 消息提示级别
logging.debug('')  # 调试级别

# 设置日志的记录等级
logging.basicConfig(level=logging.WARN)  # 调试警告级别
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小，保存日志文件的个数上限
file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式
formatter = logging.Formatter('%(levelname)s % (filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name: str 配置模式的名字 ('develop', 'product')
    :return:
    """
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)

    # 初始化redia工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask-session ,将session数据保存到redis中
    Session(app)

    # 为flask补充csrf防护
    CSRFProtect(app)

    # 注册蓝图
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')

    return app
