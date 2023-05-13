from flask import render_template, current_app as app, request, redirect, url_for
from ..controller import getUser, getUserTickets
from ..utils import validToken, detokenize
from datetime import datetime


@app.route('/myprofile', methods=['GET'])
def profile():
    auth = request.cookies.get('token', None)

    if auth:
        if not validToken(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('user_login'))
    
    uid = detokenize(auth)['id']
    user = getUser(uid=uid)
    tickets = getUserTickets(uid=uid)

    return render_template('profile.html', 
        user=user, 
        tickets=tickets,
        showTime=datetime.fromtimestamp, 
    )
