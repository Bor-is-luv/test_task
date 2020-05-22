#!/bin/bash
python manage.py db upgrade
sleep 30
uwsgi app.ini