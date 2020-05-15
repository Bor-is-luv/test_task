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

limit = int(os.environ.get('LIMIT'))
waiting_time = int(os.environ.get('WAITING_TIME'))
period = int(os.environ.get('PERIOD'))
mask_value = int(os.environ.get('MASK_VALUE'))


if mask_value < 0 or mask_value > 32:
    mask_value = 24

if waiting_time < 1:
    waiting_time = 120

if period < 1:
    period = 60

if limit < 0:
    limit = 100

if period < 12:
    job_period = 3
else:
    job_period = period/4


from apscheduler.schedulers.background import BackgroundScheduler
from utils import removal_of_restriction, clear_db


scheduler = BackgroundScheduler()
scheduler.add_job(func=removal_of_restriction, trigger="interval", seconds=2)
scheduler.add_job(func=clear_db, trigger="interval", seconds=job_period)
scheduler.start()


 