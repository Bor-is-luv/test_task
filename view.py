from app import app
from flask import request
from models import Ip
from datetime import datetime
from app import db
from utils import mask

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
        
    new_ip = mask(ip)
    ip_row = Ip(new_ip, datetime.now())
    db.session.add(ip_row)
    db.session.commit()
    return ip