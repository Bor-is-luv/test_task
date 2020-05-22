#!/bin/bash
sleep 15
python manage.py db upgrade
sleep 10
uwsgi app.ini