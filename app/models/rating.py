from ..utils import db

class Rating(db.Model):
    __tablename__='rating'
    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete="CASCADE"), nullable=False)
    comment = db.Column(db.String, nullable=False)