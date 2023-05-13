from ..utils import db

class Ticket(db.Model):
    __tablename__='tickets'
    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid', ondelete="CASCADE"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id', ondelete="CASCADE"), nullable=False)
    admits = db.Column(db.Integer, nullable=False, unique=True)
    code = db.Column(db.String, nullable=False)
    bookingTime = db.Column(db.Integer, nullable=False)
    show = db.relationship('Show', backref='tickets', lazy=True)