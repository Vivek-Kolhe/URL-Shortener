from . import db
from sqlalchemy.sql import func

class URL_DB(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    long_url = db.Column(db.String(300))
    short_url = db.Column(db.String(50))
    ip_address = db.Column(db.String(50))
    visits = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
