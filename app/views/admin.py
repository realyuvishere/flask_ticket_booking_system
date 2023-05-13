from flask import render_template, current_app as app, request, redirect, url_for
from ..controller import getAdmin, createAdmin, createVenue, getAllVenues, getAllEvents, createEvent, getVenue, getEvent, editEvent, editVenue, deleteEvent, deleteVenue, getAllShows, createShow, getShowDetails, deleteShow, getShow, editShow
from ..utils import custom_decrypt, validToken, detokenize
from . import authorizeUser
from datetime import datetime

def isAdmin(token):
    return (validToken(token) and detokenize(token)['role'] == 'admin')

@app.route('/admin', methods=['GET'])
def admin_home():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    
    def get():
        return render_template('admin_home.html', isAdmin=True)
    
    def post():
        return ''

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if validToken(auth):
            return redirect(url_for('admin_home'))
        else:
            return redirect(url_for('logout'))

    
    def getLogin():
        return render_template('admin_login.html', isAdmin=True, isAuth=True)
    
    def postLogin():
        d = request.form
        user = getAdmin(email=d['email'])
        if (user):
            if custom_decrypt(string=user.password) == d['password']:
                return authorizeUser(user=user, action=lambda:redirect(url_for('admin_home')), role='admin')
            else:
                return render_template('admin_login.html', isAdmin=True, isAuth=True, error='Wrong password')
        else:
            return render_template('admin_login.html', isAdmin=True, isAuth=True, error='No user found with these credentials')

    return {
        'GET': getLogin,
        'POST': postLogin,
    }[m]()

@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if validToken(auth):
            return redirect(url_for('admin_home'))
        else:
            return redirect(url_for('logout'))
    
    def getSignup():
        return render_template('admin_signup.html', isAdmin=True, isAuth=True)
    def postSignup():
        d = request.form
        data = {
            'name': d['name'],
            'password': d['password'],
            'email': d['email'],
        }
        user = createAdmin(data)
        if (user):
            return authorizeUser(user=user, action=lambda:redirect(url_for('admin_home')), role='admin')
        else:
            return render_template('admin_signup.html', isAdmin=True, isAuth=True, error='Something went wrong')

    return {
        'GET': getSignup,
        'POST': postSignup,
    }[m]()

@app.route('/admin/venues', methods=['GET'])
def admin_venues():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    venues = getAllVenues()

    def get():
        return render_template('admin_venues.html', isAdmin=True, venues=venues)
    
    def post():
        return ''

    return {
        'GET': get,
        # 'POST': post,
    }[m]()

@app.route('/admin/venue/create', methods=['GET', 'POST'])
def admin_create_venue():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    
    def get():
        return render_template('admin_new_venue.html', isAdmin=True)
    
    def post():
        d = request.form
        data = {
            'name': d['name'],
            'location': d['location'],
            'capacity': d['capacity'],
        }
        venue = createVenue(data)
        if (venue):
            return redirect(url_for('admin_venues'))
        else:
            return render_template('admin_new_venue.html', isAdmin=True, error="Something went wrong")

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/venue/edit/<id>', methods=['GET', 'POST'])
def admin_edit_venue(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    venue = getVenue(id=id)

    def get():
        return render_template('admin_edit_venue.html', isAdmin=True, venue=venue)
    
    def post():
        d = request.form
        data = {
            'id': id,
            'name': d['name'],
            'location': d['location'],
            'capacity': d['capacity'],
        }
        venue = editVenue(data)

        if (venue):
            return redirect(url_for('admin_venues'))
        else:
            return render_template('admin_edit_venue.html', isAdmin=True, error="Something went wrong")

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/venue/delete/<id>', methods=['GET', 'POST'])
def admin_delete_venue(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    venue = getVenue(id=id)
    
    def get():
        return render_template('admin_delete_venue.html', isAdmin=True, venue=venue)
    
    def post():
        deleteVenue(id=id)
        return redirect(url_for('admin_venues'))

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/events', methods=['GET'])
def admin_events():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    events = getAllEvents()
    
    def get():
        return render_template('admin_events.html', isAdmin=True, events=events)
    
    def post():
        return ''

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/event/create', methods=['GET', 'POST'])
def admin_create_event():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    
    def get():
        return render_template('admin_new_event.html', isAdmin=True)
    
    def post():
        d = request.form
        data = {
            'name': d['name'],
            'description': d['description'],
            'tags': d['tags'],
        }
        event = createEvent(data)
        if (event):
            return redirect(url_for('admin_events'))
        else:
            return render_template('admin_new_event.html', isAdmin=True, error="Something went wrong")

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/event/edit/<id>', methods=['GET', 'POST'])
def admin_edit_event(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    event = getEvent(id=id)

    def get():
        return render_template('admin_edit_event.html', isAdmin=True, event=event)
    
    def post():
        d = request.form
        data = {
            'id': id,
            'name': d['name'],
            'description': d['description'],
            'tags': d['tags'],
        }
        event = editEvent(data)

        if (event):
            return redirect(url_for('admin_events'))
        else:
            return render_template('admin_edit_event.html', isAdmin=True, error="Something went wrong")

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/event/delete/<id>', methods=['GET', 'POST'])
def admin_delete_event(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    
    event = getEvent(id=id)
    
    def get():
        return render_template('admin_delete_event.html', isAdmin=True, event=event)
    
    def post():
        deleteEvent(id=id)
        return redirect(url_for('admin_events'))

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/shows', methods=['GET'])
def admin_shows():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    shows = getAllShows()
    
    def get():
        return render_template('admin_shows.html', isAdmin=True, shows=shows)
    
    def post():
        return ''

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/show/create', methods=['GET', 'POST'])
def admin_create_show():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    venues = getAllVenues()
    events = getAllEvents()
    
    def get():
        return render_template('admin_new_show.html', isAdmin=True, venues=venues, events=events)
    
    def post():
        d = request.form
        data = {
            'event_id': d['event_id'],
            'venue_id': d['venue_id'],
            'timing': d['timing'],
            'price': d['price'],
            'isActive': 1 if (d['isActive'] == 'yes') else 0
        }
        show = createShow(data)
        if (show):
            return redirect(url_for('admin_shows'))
        else:
            return render_template('admin_new_show.html', isAdmin=True, venues=venues, events=events, error="Something went wrong")

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/show/edit/<id>', methods=['GET', 'POST'])
def admin_edit_show(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    venues = getAllVenues()
    events = getAllEvents()
    show = getShow(id=id)
    
    def get():
        return render_template('admin_edit_show.html', isAdmin=True, venues=venues, events=events, show=show)
    
    def post():
        d = request.form
        data = {
            'id': id,
            'event_id': d['event_id'],
            'venue_id': d['venue_id'],
            'timing': d['timing'],
            'price': d['price'],
            'isActive': 1 if (d['isActive'] == 'yes') else 0
        }
        show = editShow(data)
        if (show):
            return redirect(url_for('admin_shows'))
        else:
            return render_template('admin_edit_show.html', isAdmin=True, venues=venues, events=events, error="Something went wrong")

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/admin/show/delete/<id>', methods=['GET', 'POST'])
def admin_delete_show(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isAdmin(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('admin_login'))
    
    (show, event, venue) = getShowDetails(id=id)

    def get():
        return render_template('admin_delete_show.html', isAdmin=True, show=show, event=event, venue=venue)
    
    def post():
        deleteShow(id=id)
        return redirect(url_for('admin_shows'))

    return {
        'GET': get,
        'POST': post,
    }[m]()
