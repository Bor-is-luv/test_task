from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

limit = 10
waiting_time = 30


from apscheduler.schedulers.background import BackgroundScheduler
from utils import removal_of_restriction

scheduler = BackgroundScheduler()
scheduler.add_job(func=removal_of_restriction, trigger="interval", seconds=2)

scheduler.start()