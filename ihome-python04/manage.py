"""
@Time    : 2019/11/7 下午7:10
@Author  : chenhui
@FileName: manage.py
@Software: PyCharm
"""

from ihome import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# 创建flask的应用对象
app = create_app('develop')

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
