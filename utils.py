from app import db, limit, waiting_time
from models import Request
from datetime import datetime, timedelta
from flask import request


def removal_of_restriction():
    for row in Request.query.all():
        if datetime.now() - row.date > timedelta(seconds=waiting_time+60):
            db.session.delete(row)

    db.session.commit()


def mask(ip):
    splt = ip.split('.')
    subnet = '.'.join(splt[0:3])
    return subnet


def get_last_request(ip):
    return Request.query.filter(Request.ip==ip).order_by(Request.date.desc()).first()


def next_ip_number(ip):
    last_ip_row = get_last_request(ip) # NEED REWORK
    return last_ip_row.number + 1


def check_ip(fn):
    def wrapper(*args, **kwargs):
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr

        new_ip = mask(ip)

        last_request = get_last_request(new_ip)

        if not last_request:
            ip_row = Request(new_ip, datetime.now())
            db.session.add(ip_row)
            db.session.commit()
            return fn(*args, **kwargs)
        else:
            ip_row = Request(new_ip, datetime.now(), next_ip_number(new_ip))

            db.session.add(ip_row)
            db.session.commit()
            print(ip_row.number)

            limit_row = Request.query.filter(Request.ip==ip_row.ip).filter(Request.number==ip_row.number-limit).first()
            if limit_row is None:
                return fn(*args, **kwargs)

            if last_request.date - limit_row.date < timedelta(seconds=60) and ip_row.date - last_request.date < timedelta(seconds=waiting_time):
                return 'Too Many Requests', 429
            
            return fn(*args, **kwargs)
    return wrapper