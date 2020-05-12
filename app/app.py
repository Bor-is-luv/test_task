from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import sys
import argparse

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-l', '--limit', default=100, type=int)
    parser.add_argument ('-w', '--waiting_time', default=120, type=int)
    parser.add_argument ('-p', '--period', default=60, type=int)
    parser.add_argument ('-m', '--mask_value', default=24, type=int)
 
    return parser


parser = createParser()
namespace = parser.parse_args(sys.argv[1:])


limit = namespace.limit
waiting_time = namespace.waiting_time
period = namespace.period
mask_value = namespace.mask_value


from apscheduler.schedulers.background import BackgroundScheduler
from utils import removal_of_restriction, clear_db


scheduler = BackgroundScheduler()
scheduler.add_job(func=removal_of_restriction, trigger="interval", seconds=2)
scheduler.add_job(func=clear_db, trigger="interval", seconds=period/4)
scheduler.start()


 