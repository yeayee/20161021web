# coding:utf-8

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


# 电子邮件支持的模块功能集中在该函数中

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])  # 引入多线程发送
    thr.start()
    return thr
