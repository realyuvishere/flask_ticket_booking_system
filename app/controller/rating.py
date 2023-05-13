from ..utils import db
from ..models import Rating
from sqlalchemy import func

def createRating(data={}):
    try:
        new_rating = Rating(
            stars=data['stars'], 
            event_id=data['event_id'], 
            comment=data['comment'], 
        )
        db.session.add(new_rating)
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return new_rating

def getAllRatings():
    return db.session.query(Rating).all()

def getAvgRating(event_id=''):
    return db.session.query(func.avg(Rating.stars).label('avg_rating')).filter((Rating.event_id == event_id)).first()

def getEventRatings(event_id=''):
    rating = db.session.query(Rating).filter(Rating.event_id == event_id).all()
    return rating