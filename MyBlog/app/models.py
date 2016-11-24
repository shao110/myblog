from . import mysqldb
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from datetime import datetime
from markdown import markdown
import bleach

class User(mysqldb.Model, UserMixin):
    __tablename__ = 'users'
    id = mysqldb.Column(mysqldb.Integer, primary_key=True)
    username = mysqldb.Column(mysqldb.String(64), unique=True, index=True)
    password_hash = mysqldb.Column(mysqldb.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(mysqldb.Model):
    __tablename__ = 'posts'
    id = mysqldb.Column(mysqldb.Integer, primary_key=True)
    title = mysqldb.Column(mysqldb.String(64))
    body = mysqldb.Column(mysqldb.Text)
    body_html = mysqldb.Column(mysqldb.Text)
    summary = mysqldb.Column(mysqldb.Text)
    summary_html = mysqldb.Column(mysqldb.Text)
    timestamp = mysqldb.Column(mysqldb.DateTime, index=True, default=datetime.now)
    category_id = mysqldb.Column(mysqldb.Integer, mysqldb.ForeignKey('categorys.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                        'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                       tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_summary(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
                        'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.summary_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                       tags=allowed_tags, strip=True))

mysqldb.event.listen(Post.body, 'set', Post.on_changed_body)
mysqldb.event.listen(Post.summary, 'set', Post.on_changed_summary)

class Category(mysqldb.Model):
    __tablename__ = 'categorys'
    id = mysqldb.Column(mysqldb.Integer, primary_key=True)
    tag = mysqldb.Column(mysqldb.String(64), unique=True)
    posts = mysqldb.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return self.tag

