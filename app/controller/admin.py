from ..utils import db
from ..models import Admin
from ..utils import custom_encrypt

def createAdmin(data={}):
    if getAdmin(data['email']):
        return None
    else:
        try:
            new_user = Admin(
                email=data['email'], 
                name=data['name'], 
                password=custom_encrypt(string=data['password'])
            )
            db.session.add(new_user)
        except:
            db.session.rollback()
            raise Exception('DB error.')
        else:
            db.session.commit()
            return new_user

def deleteAdmin(uid=''):
    Admin.query.filter_by(uid=uid).delete()
    db.session.commit()
    return True

def editAdmin(data={}):
    try:
        user = getAdmin(uid=data['uid'])
        del data['uid']
        for key in data:
            setattr(user, key, data[key])
        
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True


def getAdmin(uid='', email=''):
    user = db.session.query(Admin).filter((Admin.uid == uid) | (Admin.email == email)).first()
    return user

def getMetrics():
    return ''