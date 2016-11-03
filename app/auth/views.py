# coding:utf-8

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import Users
from ..email import send_email
from werkzeug.security import generate_password_hash
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        # if not current_user.email_validated:
        #     return redirect(url_for('auth.unconfirmed'))

#
# @auth.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.from_email(form.email.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("成功登陆", category='success')
            return redirect(request.args.get("next") or url_for('main.index'))
        flash("账号或密码错误", category='error')
    return render_template('auth/login.html', form=form)


# 实现退出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


# 注册账号
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)  # 直接在这里进行哈希
        if Users.from_email(form.email.data):  # 如果该邮箱没有被注册
            flash('您的邮箱已被注册')
            return redirect(url_for('auth.register'))
        elif Users.from_username_or_email(form.username.data):
            flash('您的昵称已被注册')
            return redirect(url_for('auth.register'))
        else:
            user = Users.add(
                    username=form.username.data,
                    email=form.email.data,
                    password_hash=password)
            login_user(user)
            token = user.generate_confirmation_token()  # 形成一个临时的token，供email账号验证使用
            send_email(user.email, '确认账号', 'auth/email/confirm', user=user, token=token)
            flash('请到邮箱' + user.email + '确认注册')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# 通过访问邮件中的地址确认
@auth.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
def confirm(token):
    if current_user.email_validated:  # 邮箱认证
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已确认，谢谢注册！')
    else:
        flash('邮箱确认连接已经失效！')
    return redirect(url_for('main.index'))


# 确认账号注册，再次确认
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认账号',
               'auth/email/confirm', user=current_user, token=token)
    flash('新的确认邮件已经发送，请查收！')
    return redirect(url_for('main.index'))


# 更改密码//////////////////////////////////////////////////2016-10-28以上应该没有问题
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.update({'$set': {'password': form.password.data}})
            flash('密码已修改')
            return redirect(url_for('main.index'))
        else:
            flash('密码格式有误')
    return render_template("auth/change_password.html", form=form)


# 重设密码，要求原密码8g+
@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = Users.from_email(form.email.data)
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重设密码',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('认证邮件已发送')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


# 重设密码，获取token更8g+
@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = Users.from_email(form.email.data)
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('密码已更改')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


# 重设邮箱，获取token更8h+
@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '邮箱确认',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('确认邮件已发送至您新邮箱')
            return redirect(url_for('main.index'))
        else:
            flash('账号或密码错误')
    return render_template("auth/change_email.html", form=form)


# 重设邮箱8h+
@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('邮箱已更新')
    else:
        flash('非法请求')
    return redirect(url_for('main.index'))

# ////////////////////////////////////////2016-10-28用户认证系统搞定了，邮箱注册，密码修改