#!/bin/sh
python manage.py db upgrade
uwsgi app.ini