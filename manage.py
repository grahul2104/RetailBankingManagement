from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from app import create_app, db

app = create_app()
db.init_app(app)
# db.engine.execute("ALTER TABLE customer AUTO_INCREMENT = 123456000;")
# db.engine.execute("ALTER TABLE account AUTO_INCREMENT = 102030000;")
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
