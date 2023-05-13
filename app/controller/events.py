from ..utils import db
from ..models import Event
from .rating import getAvgRating

def createEvent(data={}):
    try:
        new_event = Event(
            name=data['name'], 
            description=data['description'], 
            tags=data['tags'], 
        )
        db.session.add(new_event)
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return new_event

def deleteEvent(id=''):
    Event.query.filter_by(id=id).delete()
    db.session.commit()
    return True

def editEvent(data={}):
    try:
        event = getEvent(id=data['id'])
        del data['id']
        for key in data:
            setattr(event, key, data[key])
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True

def getAllEvents():
    return db.session.query(Event).all()

def getEvent(id='', name='', with_rating=False):
    event = db.session.query(Event).filter((Event.id == id) | (Event.name == name)).first()
    if with_rating:
        rating = getAvgRating(event_id=id)
        return event, rating.avg_rating or 0
    else:
        return event