from app import db
from models import Ip
from datetime import datetime, timedelta
from flask import request
from app import limit


def removal_of_restriction():
    for row in Ip.query.all():
        if datetime.now() - row.date > timedelta(minutes=1):
            db.session.delete(row)
            print('delete')

    db.session.commit()


def mask(ip):
    splt = ip.split('.')
    subnet = '.'.join(splt[0:3])
    return subnet


def next_ip_number(ip):
    last_ip_row = Ip.query.filter(Ip.ip==ip).order_by(Ip.date.desc()).first() # NEED REWORK
    return last_ip_row.number + 1


def check_ip(fn):
    def wrapper(*args, **kwargs):
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr

        new_ip = mask(ip)

        if Ip.query.filter(Ip.ip==new_ip).first() is None:
            ip_row = Ip(new_ip, datetime.now())
        else:
            ip_row = Ip(new_ip, datetime.now(), next_ip_number(new_ip))

        db.session.add(ip_row)
        db.session.commit()

        limit_row = Ip.query.filter(Ip.ip==ip_row.ip).filter(Ip.number==ip_row.number-limit).first()
        if limit_row is None:
            return fn(*args, **kwargs)

        if ip_row.date - limit_row.date < timedelta(minutes=2):
            return 'Too Many Requests', 429
        
        print(ip_row.number)
        return fn(*args, **kwargs)
    return wrapper