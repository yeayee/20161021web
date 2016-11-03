# coding:utf-8

from flask import Blueprint

# 创建认证蓝本，并且把views.py引入到蓝本中

auth = Blueprint('auth', __name__)

from . import views

# 蓝本的注册依然在app文件夹中的__init__构造函数中，其实整个文件夹就是个大类，不同的蓝本就是个大函数，霍霍
