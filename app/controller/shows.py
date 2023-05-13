from ..utils import db
from ..models import Show, Event, Venue, Ticket
from sqlalchemy import func

def createShow(data={}):
    try:
        new_show = Show(
            event_id=data['event_id'],
            venue_id=data['venue_id'],
            timing=data['timing'],
            price=data['price'],
            isActive=data['isActive'],
        )
        db.session.add(new_show)
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return new_show


def getAllShows():
    return db.session.query(Show, Event, Venue).select_from(Show).join(Event).join(Venue).all()

def getAllShowsBasic():
    return db.session.query(Show).all()

def deleteShow(id=''):
    Show.query.filter_by(id=id).delete()
    db.session.commit()
    return True

def editShow(data={}):
    try:
        user = getShow(id=data['id'])
        del data['id']
        for key in data:
            setattr(user, key, data[key])
        
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True

def getShowsByEvent(event_id=''):
    shows = db.session.query(Show, Venue).select_from(Show).join(Venue).filter((Show.event_id == event_id)).all()
    return shows

def getShowsByVenue(venue_id=''):
    shows = db.session.query(Show, Event).select_from(Show).join(Event).filter((Show.venue_id == venue_id)).all()
    return shows

def getShowDetails(id=''):
    show = db.session.query(Show, Event, Venue).select_from(Show).join(Event).join(Venue).filter((Show.id == id)).first()
    return show

def getShow(id=''):
    show = db.session.query(Show).filter((Show.id == id)).first()
    return show

def getShowsByName(name=''):
    shows = db.session.query(Show, Event).select_from(Show).join(Event).filter((Event.name.like('%'+name+'%'))).all()
    return shows

def getShowsByDescription(desc=''):
    shows = db.session.query(Show, Event).select_from(Show).join(Event).filter((Event.description.like('%'+desc+'%'))).all()
    return shows

def getShowsByTags(tags=''):
    shows = db.session.query(Show, Event).select_from(Show).join(Event).filter((Event.tags.like('%'+tags+'%'))).all()
    return shows

def getShowBookedSeats(id=''):
    return db.session.query(func.sum(Ticket.admits).label('ticket_count')).filter((Ticket.show_id == id)).first()
    