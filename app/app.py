from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import sys
import argparse

import os


class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test:test@localhost:5436/test'
    SECRET_KEY = 'very secret'
    

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


#parser = createParser()
#namespace = parser.parse_args(sys.argv[1:])


#limit = namespace.limit
#waiting_time = namespace.waiting_time
#period = namespace.period
#mask_value = namespace.mask_value

limit = int(os.environ.get('LIMIT'))
waiting_time = int(os.environ.get('WAITING_TIME'))
period = int(os.environ.get('PERIOD'))
mask_value = int(os.environ.get('MASK_VALUE'))


from apscheduler.schedulers.background import BackgroundScheduler
from utils import removal_of_restriction, clear_db


scheduler = BackgroundScheduler()
scheduler.add_job(func=removal_of_restriction, trigger="interval", seconds=2)
scheduler.add_job(func=clear_db, trigger="interval", seconds=period/4)
scheduler.start()


 