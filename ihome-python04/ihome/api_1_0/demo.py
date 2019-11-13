"""
@Time    : 2019/11/9 上午9:40
@Author  : chenhui
@FileName: user.py
@Software: PyCharm
"""

from . import api


@api.route('/index')
def index():
    return 'index page'
