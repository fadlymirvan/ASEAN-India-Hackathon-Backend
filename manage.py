import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.app import create_app, db

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

manager = Manager(app=app)

migrate = Migrate(app=app, db=db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    db.create_all()
