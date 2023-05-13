from flask import render_template, current_app as app, request, redirect, make_response, url_for
from ..controller import getUser, createUser
from ..utils import custom_decrypt, tokenize, validToken

def authorizeUser(user, action, role='user'):
    res = make_response(action())
    token = tokenize(user=user, role=role)
    res.set_cookie('token', token)
    return res

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if validToken(auth):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('logout'))

    
    def getLogin():
        return render_template('login.html', isAuth=True)
    
    def postLogin():
        d = request.form
        user = getUser(email=d['email'])
        if (user):
            if custom_decrypt(string=user.password) == d['password']:
                return authorizeUser(user=user, action=lambda:redirect(url_for('home')))
            else:
                return render_template('login.html', isAuth=True, error='Wrong password')
        else:
            return render_template('login.html', isAuth=True, error='No user found with these credentials')

    return {
        'GET': getLogin,
        'POST': postLogin,
    }[m]()

@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if validToken(auth):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('logout'))
    
    def getSignup():
        return render_template('signup.html', isAuth=True)
    
    def postSignup():
        d = request.form
        try:
            data = {
                'name': d['name'],
                'phone': d['phone'],
                'password': d['password'],
                'email': d['email'],
            }

            if len(data['name']) == 0 or len(data['phone']) == 0 or len(data['email']) == 0:
                raise Exception('Please fill in all the fields')
            
            if '@' not in data['email']:
                raise Exception('Invalid email')

            if not len(data['phone']) == 10:
                raise Exception('Invalid phone number')
            
            if len(data['password']) < 6:
                raise Exception('Password length is lesser than 6')
            
            user = createUser(data)
        except BaseException as e:
            return render_template('signup.html', isAuth=True, error=e, data=data)
        else:
            if (user):
                return authorizeUser(user=user, action=lambda:redirect(url_for('home')))
            else:
                return render_template('signup.html', isAuth=True, error='Something went wrong', data=data)

    return {
        'GET': getSignup,
        'POST': postSignup,
    }[m]()

@app.route('/logout')
def logout():
    res = make_response(redirect(url_for('user_login')))
    res.delete_cookie('token')
    return res
