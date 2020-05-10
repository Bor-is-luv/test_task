from app import db


class Ip(db.Model):
    __tablename__ = 'ip'
    ip = db.Column(db.String, primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)

    def __init__(self, ip, date):
        self.ip = ip
        self.date = date

    def __repr__(self):
        return f"<Ip({self.ip} {self.date})>"
