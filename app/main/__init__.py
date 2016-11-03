# coding:utf-8

from flask import Blueprint

main = Blueprint('main', __name__)  # 创建一个名称为main的蓝本,在app.__init__中进行蓝本注册，若想取消该功能，只需要取消注册即可

from . import views, errors  # 把views.py, errors.py两个函数引入到蓝本中

# 下面的意义不明，仅仅用在测试？ Permission里面的是全局变量，怎么还要导入？
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
