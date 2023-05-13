from ..utils import db
from ..models import Venue

def createVenue(data={}):
    try:
        new_venue = Venue(
            name=data['name'], 
            location=data['location'], 
            capacity=data['capacity'], 
        )
        db.session.add(new_venue)
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return new_venue

def deleteVenue(id=''):
    Venue.query.filter_by(id=id).delete()
    db.session.commit()
    return True

def editVenue(data={}):
    try:
        venue = getVenue(id=data['id'])
        print(venue)
        del data['id']
        for key in data:
            setattr(venue, key, data[key])
        
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True

def getAllVenues():
    return db.session.query(Venue).all()

def getVenue(id='', name='', location=''):
    venue = db.session.query(Venue).filter((Venue.id == id) | (Venue.name == name) | (Venue.location == location)).first()
    return venue