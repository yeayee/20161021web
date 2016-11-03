# coding:utf-8

from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileAdminForm, PostForm, CommentForm
from .. import mongo
# from ..models import Permission, Role, User, Post,Comment
from ..models import Permission
from ..decorators import admin_required, permission_required


@main.route('/')  # 11a+实现博客首页
def index():
    return render_template('index.html')

#
# @main.route('/user/<username>')
# def user(username):
#     # user = User.query.filter_by(username=username).first_or_404()  # 这鸡毛玩意也是数据库操作
#     pass
#     return render_template('user.html', user=user)

#
# # 管理员级别的用户资料编辑
# @main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_profile_admin(id):
#     user = User.query.get_or_404(id)
#     form = EditProfileAdminForm(user=user)
#     if form.validate_on_submit():
#         user.email = form.email.data
#         user.username = form.username.data
#         user.confirmed = form.confirmed.data
#         # user.role = Role.query.get(form.role.data)  # 在form中暂时注销掉
#         user.score_me = form.score.data  # 提交积分数据
#         db.session.add(user)
#         flash('资料已更新')
#         return redirect(url_for('.user', username=user.username))
#     form.email.data = user.email
#     form.username.data = user.username
#     form.confirmed.data = user.confirmed
#     form.role.data = user.role_id
#     form.score.data = user.score_me  # 逐条显示表单
#     return render_template('edit_profile.html', form=form, user=user)


@main.route('/anli/<qanda>')  # 发布只需要后台执行就行，无需手动操作，更新图片就可自动更新
def anli(qanda):
    # question='专业知识/2014/上午/问题/14C_01.jpg'
    # 还需要一个处理名称的函数？
    question = '专业知识/2014/上午/问题/' + qanda + '.jpg'
    answer = '专业知识/2014/上午/答案/' + qanda + '.jpg'
    return render_template('question.html', question=question, answer=answer)

#  一下为博客的文章发布提交相关内容，暂时不急
# # 博客首页路由11a+
# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = PostForm()
#     if current_user.can(Permission.WRITE_ARTICLES) and \
#             form.validate_on_submit():
#         post = Post(body=form.body.data,
#                     author=current_user._get_current_object())
#         db.session.add(post)
#         return redirect(url_for('.index'))
#     page = request.args.get('page', 1, type=int)
#     pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     return render_template('index.html', form=form, posts=posts,
#                            pagination=pagination)
#
#
# @main.route('/post/<int:id>', methods=['GET', 'POST'])
# def post(id):
#     post = Post.query.get_or_404(id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comment(body=form.body.data,
#                           post=post,
#                           author=current_user._get_current_object())
#         db.session.add(comment)
#         flash('Your comment has been published.')
#         return redirect(url_for('.post', id=post.id, page=-1))
#     page = request.args.get('page', 1, type=int)
#     if page == -1:
#         page = (post.comments.count() - 1) // \
#             current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
#     pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
#         page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
#         error_out=False)
#     comments = pagination.items
#     return render_template('post.html', posts=[post], form=form,
#                            comments=comments, pagination=pagination)
#
#
# @main.route('/edit/<int:id>', methods=['GET', 'POST'])  # 11h+文章进行编辑
# @login_required
# def edit(id):
#     post = Post.query.get_or_404(id)
#     if current_user != post.author and \
#             not current_user.can(Permission.ADMINISTER):
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.body = form.body.data
#         db.session.add(post)
#         flash('文章已更新')
#         return redirect(url_for('.post', id=post.id))
#     form.body.data = post.body
#     return render_template('edit_post.html', form=form)
#
#
# @main.route('/moderate')   # 13b+评论管理路由
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate():
#     page = request.args.get('page', 1, type=int)
#     pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
#         error_out=False)
#     comments = pagination.items
#     return render_template('moderate.html', comments=comments,
#                            pagination=pagination, page=page)
#
#
# @main.route('/moderate/enable/<int:id>')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate_enable(id):
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = False
#     db.session.add(comment)
#     return redirect(url_for('.moderate',
#                             page=request.args.get('page', 1, type=int)))
#
#
# @main.route('/moderate/disable/<int:id>')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate_disable(id):
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = True
#     db.session.add(comment)
#     return redirect(url_for('.moderate',
#                             page=request.args.get('page', 1, type=int)))
