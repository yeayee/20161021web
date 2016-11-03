# coding:utf-8
# 2016-10-21决定上MongoDB，从今天开始的修改就采用改写的模式
import os
from app import create_app
from flask_script import Manager, Shell
from app import init_db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return app


@manager.command
def init_db():
    """
    :return:暂时没有什么鸟用
    """
    try:
        init_db()
    except:
        pass

manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
