# coding:utf-8
from werkzeug.security import check_password_hash
from flask import current_app, url_for, render_template, g  # 发送邮件，修改账户信息！
from bson.objectid import ObjectId
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from app import mongo
from pymongo import IndexModel, ASCENDING
from copy import deepcopy
from app import config


# 数据库模型支持的模块功能集中在该函数中，按照大牛的资料进行重构
# print(config.get('default').MONGO_COLLECTION_PREFIX)  # 从config中提取参数，暂时只会这样提取


class Permission:  # 9a+权限常量，虽然可能没有用，但是后面还需要用到，所暂时删不掉。
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class MongoBase(object):  # 类似于生成关系型数据库中的db.Model

    _id = id = None

    def __getattr__(self, key):
        """
        :param key: 获取selfuser游标中的键，从下面self.Values赋值过程中可以看出
        :return:
        """
        if key in self.values:
            return self.values[key]
        else:
            raise AttributeError()

    #    def __init__(self):  # 如果没有预定义的键，则不进行操作，比较严格
    #        for key in self.default.iterkeys():
    #            setattr(self, key, property(self.getter, self.setter, None))

    @classmethod
    def create_collection(self):
        """
        :return:初始化数据库，这个对于mongodb来说确实有点多余，在manage.py中实现
        """
        mongo.db.create_collection(self.collection)
        collection = self._get_collection()
        collection.create_indexes(self.indices)

    @classmethod
    def _get_collection(self):
        """
        :return: 获取self自身的集合名
        """
        return mongo.db.get_collection(self.collection)

    def insert(self):
        """
        :return:插入一个新的用户，没有返回值
        """
        assert not self._id
        collection = self._get_collection()
        res = collection.insert_one(self.values)
        self._id = res.inserted_id

    def update(self, update):
        """
        :param update:更新一个update数据，也没有返回值
        :return:
        """
        assert self._id
        collection = self._get_collection()
        collection.update_one({'_id': self._id}, update)


def create_all_collections():
    for cls in [MongoUser]:
        cls.create_collection()


class MongoUser(MongoBase, UserMixin):  # 从上面的对象中继承，同时联合longin的类UserMixin一起搞基
    collection = config.get('default').MONGO_COLLECTION_PREFIX + 'user'  # 在上面超类中调用改参数，进行生成数据库
    indices = [
        IndexModel([('username', ASCENDING)], unique=True, sparse=True),
        IndexModel([('email', ASCENDING)], unique=True)
    ]  # 定义用户的主键，对于现阶段而言似乎并没有必要

    # try: 暂时不要在这里初始化了，避免不必要的麻烦，没有序列并不影响查询的速度
    #     collections = mongo.db.create_collection(collection)
    #     collections.create_indexes(indices)
    # except:
    #     pass

    default = {
        'username': None,
        'email': None,
        'password_hash': None,
        'scores': 1000,
        'role': 'user',
        'registered_on': None,
        'email_validated': False,

    }

    def __init__(self, _id=None, **kwargs):
        MongoBase.__init__(self)
        self.values = deepcopy(self.default)
        if _id:
            self._id = _id
            self.values.update(**kwargs)
        else:
            self.values['registered_on'] = datetime.now()
            self.values.update(**kwargs)

    @classmethod
    def from_email(cls, email):  # 通过邮箱查找，并返回user
        collection = cls._get_collection()
        user = collection.find_one({'email': email})
        if user:
            return MongoUser(**user)
        else:
            return None

    @classmethod
    def from_username_or_email(cls, user):  # 通过邮箱或者昵称查找，并返回user
        collection = cls._get_collection()
        usero = collection.find_one(
                {'$or': [{'email': user}, {'username': user}]})
        if usero:
            return MongoUser(**usero)
        else:
            return None

    @classmethod
    def from_id(cls, stringid):  # 通过Id，转换ID为ObjectId，然后通过_id进行查找，并返回user
        id = ObjectId(stringid)
        collection = cls._get_collection()
        user = collection.find_one({'_id': id})
        if user:
            return MongoUser(**user)
        else:
            return None

    def get_id(self):  # 这个必须有，获取用户_id和关系型数据库大不同
        return str(self._id)

    def as_dict(self):
        return self.values

    # /////////////Web 实战///////////////2010-10-28测试成功,但是很多东西还是没有吃透！
    def verify_password(self, password):
        """
        :param password:这里的password主要是对表单提交的密码进行验证
        :return:
        """

        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': str(self._id)})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != str(self._id):
            return False
        self.update({'$set': {'email_validated': True}})
        self.values['email_validated'] = True
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': str(self._id)})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != str(self._id):
            return False
        self.values['password '] = new_password
        self.update({'$set': {'password': new_password}})
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': str(self._id), 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.find_one({'email': new_email}) is not None:
            return False
        self.values['email'] = new_email
        self.update({'$set': {'email': new_email}})
        return True

    def ping(self):  # 10a+ 刷新用户最后的访问时间
        self.values['last_seen'] = datetime.now() # datetime.now()
        self.update({'$set': {'last_seen': datetime.now()}})

    def __repr__(self):
        return ' username {} email {}'.format(*[getattr(self, key) for key in ['username', 'email']])


class Users(object):
    @classmethod
    def add(cls, **kwargs):
        user = MongoUser(**kwargs)
        user.insert()
        return user

    @classmethod
    def update(cls, update, **kwargs):  # 这个更新暂时还没有想到用在哪里，关于用户的个人信息增量的时候可能会用到！
        '''
        :param update:参数格式参考 update({'$set': {'email_validated': True}})，
        :param kwargs:
        :return:
        '''
        user = MongoUser(**kwargs)
        user.update(update)
        return user

    @classmethod
    def from_email(cls, email):
        return MongoUser.from_email(email=email)

    @classmethod
    def from_username_or_email(cls, user):
        return MongoUser.from_username_or_email(user)

    @classmethod
    def from_id(cls, user_id):
        return MongoUser.from_id(stringid=user_id)

