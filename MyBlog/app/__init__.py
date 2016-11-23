from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_wtf.csrf import CsrfProtect

mysqldb = SQLAlchemy()
pagedown = PageDown()
bootstrap = Bootstrap()
csrf = CsrfProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    login_manager.init_app(app)
    mysqldb.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app