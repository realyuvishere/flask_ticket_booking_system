from ..utils import db
from ..models import User
from ..utils import custom_encrypt

def createUser(data={}):
    if getUser(data['email']):
        return None
    else:
        try:
            new_user = User(
                phone=data['phone'], 
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

def deleteUser(uid=''):
    User.query.filter_by(uid=uid).delete()
    db.session.commit()
    return True

def editUser(data={}):
    try:
        user = getUser(uid=data['id'])
        del data['id']
        for key in data:
            setattr(user, key, data[key])
        
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True


def getUser(uid='', email=''):
    user = db.session.query(User).filter((User.uid == uid) | (User.email == email)).first()
    return user