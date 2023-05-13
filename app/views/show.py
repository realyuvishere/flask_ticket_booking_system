from flask import render_template, current_app as app, request, redirect, url_for
from ..utils import validToken
from ..controller import getShowsByVenue, getShowsByEvent, getShowDetails, getEvent, getVenue, getShowBookedSeats

@app.route('/venue/<id>', methods=['GET', 'POST'])
def venue_shows(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))
    
    venueShows = getShowsByVenue(venue_id=id)
    venue = getVenue(id=id)

    def get():
        return render_template('venue_shows.html', data=venueShows, venue=venue)
    
    def post():
        return ''
        

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/event/<id>', methods=['GET'])
def event_shows(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))
    
    
    def get():
        try:

            eventShows = getShowsByEvent(event_id=id)
            event, rating = getEvent(id=id, with_rating=True)
            event.avg_rating = rating

        except:
            return render_template('event_shows.html', error='Something went wrong')
        else:
            return render_template('event_shows.html', data=eventShows, event=event)

        

    return {
        'GET': get
    }[m]()

@app.route('/show/<id>', methods=['GET', 'POST'])
def show_details(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))
    
    show, event, venue = getShowDetails(id=id)

    count = getShowBookedSeats(id=id)[0]

    occupied_seats = 0 if count==None else count
    
    def get():
        return render_template('show_details.html', show=show, event=event, venue=venue, occupied_seats=occupied_seats)
    
    def post():
        return ''
        

    return {
        'GET': get,
        'POST': post,
    }[m]()

