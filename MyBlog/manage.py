from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, mysqldb
from app.models import User
from config import Config



app = create_app(Config)
manager = Manager(app)
migrate = Migrate(app, mysqldb)

def make_shell_context():
    return dict(app=app, mysqldb=mysqldb, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()
