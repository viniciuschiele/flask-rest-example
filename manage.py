import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_script import Server
from stash_api import db
from stash_api.app import create_app

env = os.environ.get('APP_ENV', 'development')

app = create_app(env)

migrate = Migrate(app, db)

manager = Manager(app, False)
manager.add_command('runserver', Server('0.0.0.0'))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
