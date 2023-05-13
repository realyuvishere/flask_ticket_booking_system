from ..utils import db

class Show(db.Model):
    __tablename__='shows'
    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete="CASCADE"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete="CASCADE"), nullable=False)
    timing = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Integer, nullable=False)