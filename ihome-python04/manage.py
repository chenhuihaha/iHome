"""
@Time    : 2019/11/7 下午7:10
@Author  : chenhui
@FileName: manage.py
@Software: PyCharm
"""

from flask_session import Session
from flask_wtf import CSRFProtect
from ihome import create_app

import redis

# 创建flask的应用对象
app = create_app('develop')



# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 利用flask-session ,将session数据保存到redis中
Session(app)

# 为flask补充csrf防护
CSRFProtect(app)


@app.route('/index')
def index():
    return 'index page'


if __name__ == '__main__':
    app.run()
