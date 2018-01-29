import datetime
from webapp import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    chassis_id = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, make, model, year, chassis_id, price, last_updated):
        self.make = make
        self.model = model
        self.year = year
        self.chassis_id = chassis_id
        self.price = price
        self.last_updated = last_updated if last_updated is not None else datetime.datetime.now()
