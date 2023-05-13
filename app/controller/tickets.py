from ..utils import db
from ..models import Ticket
from hashlib import sha256
from base64 import b64encode
from time import time_ns
from sqlalchemy import desc

def createTicket(data={}):
    try:
        data['bookingTime'] = time_ns()
        data['code'] = sha256(f'{time_ns()}_{data["uid"]}'.encode('utf-8')).hexdigest()[:8]
        new_ticket = Ticket(
            uid=data['uid'], 
            show_id=data['show_id'], 
            code=data['code'], 
            admits=data['admits'], 
            bookingTime=data['bookingTime'], 
        )
        db.session.add(new_ticket)
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return new_ticket

def deleteTicket(id=''):
    Ticket.query.filter_by(id=id).delete()
    db.session.commit()
    return True

def getAllTickets():
    return db.session.query(Ticket).all()

def getTicket(id='', show_id='', code=''):
    ticket = db.session.query(Ticket).filter((Ticket.id == id) | (Ticket.show_id == show_id) | (Ticket.code == code)).first()
    return ticket

def getUserTickets(uid=''):
    return db.session.query(Ticket).filter((Ticket.uid == uid)).order_by(desc(Ticket.bookingTime)).all()
