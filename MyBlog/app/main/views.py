from flask import render_template, redirect, flash, url_for, request, current_app
from . import main
from app import mysqldb
from ..models import User, Post, Category
from .forms import LoginForm, PostForm
from flask_login import login_user, login_required, logout_user, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    categorys = Category.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POST_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination, categorys=categorys)


@main.route('/about')
def about_me():
    return render_template('about.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = PostForm()
    #categorys = Category.query.all()
    if current_user.is_authenticated and form.validate_on_submit():
        posts = Post(title=form.title.data, body=form.body.data, summary=form.summary.data,
                     category_id=form.category.data)
        mysqldb.session.add(posts)
        return redirect(url_for('main.index'))
    return render_template('write.html', form=form)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@main.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    mysqldb.session.delete(post)
    return redirect(url_for('main.index'))

@main.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if current_user.is_authenticated and form.validate_on_submit():
        post.title = form.title.data
        post.summary = form.summary.data
        post.body = form.body.data
        post.category_id = form.category.data
        mysqldb.session.add(post)
        return redirect(url_for('main.post', id=post.id))
    form.title.data = post.title
    form.summary.data = post.summary
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('edit.html', form=form, post=post)

@main.route('/category/<tag>')
def category(tag):
    category = Category.query.filter_by(tag=tag).first()
    page = request.args.get('page', 1, type=int)
    pagination = category.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POST_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('category.html', posts=posts, pagination=pagination,
                           category=category)
