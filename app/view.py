from app import app
from app import db
from utils import check_ip


@app.route('/', methods=['GET', 'POST'])
@check_ip
def index():
    return 'ok', 200