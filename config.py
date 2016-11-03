# coding:utf-8
# 默认为开发环境，等发布的时候改为生产环境，此次学习用的是7-a的示例，从数据开始整理！
# 把没有用的命令，注释掉，然后观察界面的变化。


import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径： D:\pywork\20161010web,这一招部分系统


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MIMA is Nidaye'  # 密码放在环境变量中进行读取
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.yeah.net'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 密码放在环境变量中进行读取
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 密码放在环境变量中进行读取
    FLASKY_MAIL_SUBJECT_PREFIX = '注册土木'
    FLASKY_MAIL_SENDER = '注册土木<yeayee@yeah.net>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')  # Flask管理员的邮箱
    MAIL_USERNAME = 'yeayee'  # 由于环境变量的设置在重启后需要重新定义，所以还是直接定义
    MAIL_PASSWORD = 'LOVE1005'
    FLASKY_ADMIN = '85362057@qq.com'
    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 10

    @staticmethod  # 这个静态方法是个什么鬼？
    def init_app(app):
        pass


# 三种不同的开发环境采用不同的数据库
class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                           'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # 数据库的路径，默认的端口就是27017，这种连接的方式有点高端了
    MONGO_DBNAME = 'civil'  # 建立一个名字为civil的数据库
    MONGODB_PORT = 27017
    MONGO_URI = 'mongodb://localhost/' + MONGO_DBNAME
    MONGO_COLLECTION_PREFIX = 'civil_flask_blog_'
    UPLOAD_FOLDER = basedir + '/app/uploads/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])  #为毛是个几何呢？


# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
#
#
# class ProductionConfig(Config):
#      SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,

    'default': DevelopmentConfig
}
