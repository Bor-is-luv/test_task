from app import db


class Ip(db.Model):
    __tablename__ = 'ip'
    ip = db.Column(db.String, primary_key=True,)
    date = db.Column(db.DateTime, primary_key=True)
    number = db.Column(db.Integer)

    def __init__(self, ip, date, number=1):
        self.ip = ip
        self.date = date
        self.number = number

    def __repr__(self):
        return f"<Ip({self.ip} {self.date})>"
