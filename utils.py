from app import db, limit, waiting_time, period, mask_value
from models import Request, Subnet
from datetime import datetime, timedelta
from flask import request


def generate_mask(mask_value):
    str_mask = ''.join(['1' for i in range(mask_value)])
    while len(str_mask) < 32:
        str_mask = str_mask + '0'

    print(str_mask, ' str mask')
    bin_mask = bin(int(str_mask, base=2))[2:]
    split_bin_mask = [bin_mask[i:i+8] for i in range(0, len(bin_mask), 8)]
    for i in range(len(split_bin_mask)):
        split_bin_mask[i] = int(split_bin_mask[i],base=2)
    return split_bin_mask


def clear_db():
    for subnet in Subnet.query.all():
        for rqst in subnet.requests:
            if not subnet.allowed:
                db.session.delete(rqst)
            else:
                if datetime.now() - rqst.date >= timedelta(seconds=period):
                    db.session.delete(rqst)

    db.session.commit()


def removal_of_restriction():
    for subnet in Subnet.query.all():
        if not subnet.allowed:
            if datetime.now() - subnet.start_of_restriction >= timedelta(seconds=waiting_time):
                subnet.allowed = True
                subnet.start_of_restriction = None

    db.session.commit()


def mask(ip, mask_value):
    splt = ip.split('.')
    for i in range(len(splt)):
        splt[i] = int(splt[i])
    int_mask = generate_mask(mask_value)
    subnet = []
    print(int_mask, ' int_mask')
    print(splt, ' splt ip')
    for i in range(len(int_mask)):
        subnet.append(str(int_mask[i] & splt[i]))
    subnet = '.'.join(subnet)
    print(subnet, ' return subnet')
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

        new_ip = mask(ip, mask_value)

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
        elif rqst.date - limit_row.date < timedelta(seconds=period):
            subnet.allowed = False
            subnet.start_of_restriction = datetime.now()
            db.session.add(subnet)
            db.session.commit()
            return 'Too Many Requests', 429
            
        return fn(*args, **kwargs)
    return wrapper