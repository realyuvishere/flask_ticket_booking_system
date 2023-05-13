from flask import render_template, current_app as app, request, redirect, url_for
from ..utils import validToken, detokenize
from ..controller import getShowDetails, getShowBookedSeats, createTicket, getTicket
from datetime import datetime

@app.route('/booking_confirmed/<code>', methods=['GET'])
def booking_confirmed(code):
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))
    
    
    def get():
        return render_template('show_booking_confirmed.html', code=code)
    
        

    return {
        'GET': get,
    }[m]()

@app.route('/book/<id>', methods=['GET', 'POST'])
def book_tickets(id):
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
        return render_template('show_booking.html', show=show, event=event, venue=venue, occupied_seats=occupied_seats)
    
    def post():
        if ((show.isActive == 1) and (occupied_seats < venue.capacity)):
            try:
                d = request.form
                
                if (not d['seats'].isnumeric()):
                    raise Exception('Number of seats field is not a number')
                
                data = {
                    'uid': detokenize(auth)['id'],
                    'show_id': id,
                    'admits': d['seats'],
                }

            except:
                return render_template('show_booking.html', show=show, event=event, venue=venue, occupied_seats=occupied_seats, error='Please provide valid inputs.')
            else:
                ticket = createTicket(data)

                if (ticket):
                    return redirect(url_for('booking_confirmed', code=data['code']))
                else:
                    return render_template('show_booking.html', show=show, event=event, venue=venue, occupied_seats=occupied_seats, error='Something went wrong, please try again')
        else:
            return 'Wrong method.'
        

    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/ticket/<code>', methods=['GET'])
def show_ticket(code):
    m = request.method
    auth = request.cookies.get('token', None)


    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))
    
    
    def get():
        try:
            ticket = getTicket(code=code)
        except BaseException as e:
            return render_template('_404.html', error=e)
        else:
            show, event, venue = getShowDetails(id=ticket.show_id)
            return render_template('show_ticket.html', ticket=ticket, show=show, event=event, venue=venue, showTime=datetime.fromtimestamp)
    
    return {
        'GET': get,
    }[m]()
