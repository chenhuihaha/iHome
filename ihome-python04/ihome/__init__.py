"""
@Time    : 2019/11/8 下午7:42
@Author  : chenhui
@FileName: __init__.py.py
@Software: PyCharm
"""
from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy


# 数据库
db = SQLAlchemy()


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

    return app