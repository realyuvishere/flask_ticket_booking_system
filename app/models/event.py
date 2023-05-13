from ..utils import db

class Event(db.Model):
    __tablename__='events'
    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)
    shows = db.relationship('Show', backref='event', lazy=True)