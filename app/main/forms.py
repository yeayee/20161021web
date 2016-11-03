# coding:utf-8

from flask_wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,IntegerField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError



class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):  # 10.3.2+管理员级别的用户编辑
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('昵称', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          '必须不能使用纯数字')])
    confirmed = BooleanField('认证')
    role = SelectField('角色', coerce=int)
    score = IntegerField('积分')  # 新增加积分更改的表单
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        # self.role.choices = [(role.id, role.name)
        #                      for role in Role.query.order_by(Role.name).all()]  # 给出角色的列表供管理员调整，稍后修改
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱有误')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('昵称有误')


class PostForm(Form):  # 11a+增加一个用户提交博客文章的表单
    body = TextAreaField("说说您的看法", validators=[Required()])
    submit = SubmitField('提交')


class CommentForm(Form):  # 13a+增加一个用户评论的表单
    body = StringField('说说您的看法', validators=[Required()])
    submit = SubmitField('提交')
