from app import db, limit, waiting_time
from models import Request, Subnet
from datetime import datetime, timedelta
from flask import request


def removal_of_restriction():
    for subnet in Subnet.query.all():
        if not subnet.allowed:
            if datetime.now() - subnet.start_of_restriction >= timedelta(seconds=waiting_time):
                subnet.allowed = True
                subnet.start_of_restriction = None

    db.session.commit()


def mask(ip):
    splt = ip.split('.')
    subnet = '.'.join(splt[0:3])
    return subnet


def get_last_request(ip):
    return Request.query.filter(Request.ip==ip).order_by(Request.date.desc()).first()


def next_request_number(ip):
    last_ip_row = get_last_request(ip) # NEED REWORK
    if last_ip_row is None:
        return 1
    else:
        return last_ip_row.number + 1


def check_ip(fn):
    def wrapper(*args, **kwargs):
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr

        new_ip = mask(ip)

        exist = Subnet.query.filter(Subnet.ip==new_ip).first()
        if not exist:
            subnet = Subnet(new_ip)
        else:
            subnet = exist 
            
        rqst = Request(new_ip, datetime.now(), next_request_number(new_ip))    
        subnet.requests.append(rqst)

        db.session.add(rqst, subnet)
        db.session.commit()

        if not subnet.allowed:
            return 'Too Many Requests', 429

        limit_row = Request.query.filter(Request.ip==rqst.ip).filter(Request.number==rqst.number-limit).first()
        if limit_row is None:
            return fn(*args, **kwargs)
        elif rqst.date - limit_row.date < timedelta(seconds=10):
            subnet.allowed = False
            subnet.start_of_restriction = datetime.now()
            db.session.add(subnet)
            db.session.commit()
            return 'Too Many Requests', 429
            
        return fn(*args, **kwargs)
    return wrapper