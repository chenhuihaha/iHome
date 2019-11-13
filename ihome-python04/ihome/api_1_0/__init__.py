"""
@Time    : 2019/11/9 上午9:39
@Author  : chenhui
@FileName: __init__.py.py
@Software: PyCharm
"""

from flask import Blueprint


api = Blueprint('api_1_0', __name__)
from . import demo
# 导入蓝图的视图

