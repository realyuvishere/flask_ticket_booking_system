from ..utils import db

class User(db.Model):
    __tablename__='users'
    uid = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)