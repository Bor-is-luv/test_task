#!/bin/bash
sleep 10
python manage.py db upgrade
sleep 10
uwsgi app.ini