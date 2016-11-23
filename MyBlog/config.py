import re

class Config:
    SECRET_KEY = 'SHAO'
    CSRF_ENABLED = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/myblog'
    POST_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass
