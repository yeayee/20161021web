# coding:utf-8
# 这里的注册系统是数据库操作的关键，搞定这个基本就可以搞定longin扩展
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .. import mongo
from ..models import Users


class LoginForm(Form):  # 登录表单
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住')
    submit = SubmitField('登录')


class RegistrationForm(Form):  # 用户注册表单
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    username = StringField('昵称', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '必须不能使用纯数字')])
    password = PasswordField('输入密码', validators=[
        Required(), EqualTo('password2', message='密码必须相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        user = mongo.db.users

        if user.find_one({"_id": field.data}):
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        user = mongo.db.users
        if user.find_one({"name": field.data}):
            raise ValidationError('昵称已经存在')


class ChangePasswordForm(Form):  # 8f+更改密码
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='密码必须相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('更改')


class PasswordResetRequestForm(Form):  # 8g+重设密码
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    submit = SubmitField('提交')


class PasswordResetForm(Form):  # 8g+重设密码
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                          Email()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='密码必须相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('重设')

    def validate_email(self, field):
        if Users.from_email(field.data) is None:
            raise ValidationError('邮箱有误')


class ChangeEmailForm(Form):  # 8h+修改电子邮件
    email = StringField('新邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('更改')

    def validate_email(self, field):
        if Users.from_email(field.data):
            raise ValidationError('邮箱有误')
