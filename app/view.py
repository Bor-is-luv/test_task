from app import app
from app import db
from utils import check_ip
from flask import render_template


@app.route('/', methods=['GET', 'POST'])
@check_ip
def index():
    return render_template('index.html')