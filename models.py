from app import db


class Subnet(db.Model):
    __tablename__ = 'subnet'
    ip = db.Column(db.String, primary_key=True)
    allowed = db.Column(db.Boolean, default=True)
    start_of_restriction = db.Column(db.DateTime, nullable=True)
    requests = db.relationship('Request', backref='subnet', lazy=True)

    def __init__(self, ip, allowed=True, start_of_restriction=None):
        self.ip = ip
        self.allowed = allowed
        self.start_of_restriction = start_of_restriction

    def __repr__(self):
        return f"<Subnet({self.ip} {self.date})>"


class Request(db.Model):
    __tablename__ = 'request'
    ip = db.Column(db.String, db.ForeignKey('subnet.ip'), nullable=False, primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    number = db.Column(db.Integer, nullable=False)

    def __init__(self, ip, date, number=1):
        self.ip = ip
        self.date = date
        self.number = number

    def __repr__(self):
        return f"<Request({self.ip} {self.date})>"
