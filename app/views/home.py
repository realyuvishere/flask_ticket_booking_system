from flask import render_template, current_app as app, request, redirect, make_response, url_for
from ..utils import validToken
from ..controller import getAllVenues, getAllEvents, getShowsByDescription, getShowsByName, getShowsByTags, getEvent, createRating

@app.route('/', methods=['GET'])
def home():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))

    venues = getAllVenues()
    events = getAllEvents()

    def get():
        return render_template('home.html', venues=venues, events=events)
        

    return {
        'GET': get,
    }[m]()

@app.route('/search', methods=['GET', 'POST'])
def search():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))
    
    def get():
        return render_template('search.html')
    
    def post():
        d = request.form

        query = d['search']
        filter_by = d['filter']

        try: 
            result = {
                'name': getShowsByName,
                'description': getShowsByDescription,
                'tags': getShowsByTags,
            }[filter_by](query)
        except:
            return render_template('search.html', error='Something went wrong, try again.')
        
        if (result):
            return render_template('search.html', result=result)
        else:
            return render_template('search.html', error="No results")

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/rating/<id>', methods=['GET', 'POST'])
def event_rating(id):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))
    
    event = getEvent(id=id)
    
    def get():
        return render_template('rating.html', event=event)
    
    def post():
        d = request.form
        data = {
            'stars': d['stars'],
            'event_id': id,
            'comment': d['comment'],
        }

        rated = createRating(data=data)

        if (rated):
            return redirect(url_for('home'))
        else:
            return render_template('rating.html', event=event, error="Something went wrong, try again.")
        

    return {
        'GET': get,
        'POST': post,
    }[m]()

