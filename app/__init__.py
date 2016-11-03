# coding:utf-8

from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_mail import Mail  # 初始化Flask-mail
from flask_moment import Moment
from flask_pymongo import PyMongo
from config import config
from flask_login import LoginManager  # 8c+登录模型


bootstrap = Bootstrap()  # 没有指向性的初始化
mail = Mail()
moment = Moment()
mongo = PyMongo()

login_manager = LoginManager()  # 8c+增加用户登录初始化
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'  # 与视图模板相对应
login_manager.login_message = "请从本页登陆"


def create_app(config_name):
    '''
    :param config_name:app而是一个对象，正式py大法万物皆对象的精髓
    。create_app() 函数就是程序的工厂函数，接受一个参数，是程序使用的配置名。配置类在 config.py文件中定义
    配置对象，可以通过名字从 config 字典中选择，默认的是 'default': DevelopmentConfig
    :return:
    '''
    app = Flask(__name__)  # 第一次实例化一个app，和下面返回的app不同
    app.config.from_object(config[config_name])  # app.config 配置对象提供的 from_object() 方法直接导入程序
    config[config_name].init_app(app)
    # print(config_name)  # 调试出来为：default，也就是按开发环境进行config配置
    bootstrap.init_app(app)  # 实例化bootstrap扩展
    mail.init_app(app)  # 实例化邮件相关扩展
    moment.init_app(app)  # 实例化本地化时间扩展
    login_manager.init_app(app)  # 8c+初始化Flasklogin
    app.config.from_object('config')
    mongo.init_app(app)

    # 下面就是分别注册main、auth两个蓝本，有必要的话可以单独建立一个admin的蓝本，用来管理管理员权限
    from .main import main as main_blueprint  # 导入main并注册main蓝本
    # main = Blueprint('main', __name__)  # 也就是main.__init__中的main(生成蓝图)
    app.register_blueprint(main_blueprint)  # 把main as main_blueprint注册到app，然后返回一个app对象
    from .auth import auth as auth_blueprint  # 注册蓝本auth
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # 还要把Url锁定为'/auth'
    return app  # 该app已经不是最初实例化的app，而是一个包含各种插件功能的app

from .models import create_all_collections
def init_db():
    models.create_all_collections()

from .models import Users   # 奇怪，又可以使用了，什么情况啊！

@login_manager.user_loader
def load_user(user_id):
    return Users.from_id(user_id)
