from flask import Flask, g, session, request, render_template, flash, redirect, url_for
from flaskext.openid import OpenID
from db.documents import User, Question
from mongoengine import *

app = Flask(__name__)
app.debug = True
app.secret_key = 'very_secret_key'
oid = OpenID(app)

@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        try:
            g.user = User.objects.get(openid=session['openid'])
        except:
            g.user = None

@app.route('/')
@app.route('/questions/')
def index():
    return render_template('index.html', questions = Question.objects, title = 'Home')

@app.route('/questions/<id>/')
def question_details(id):
    return "question details"

@app.route('/questions/ask/')
def ask_question():
    return "ask"

@app.route('/questions/unanswered/')
def unanswered_questions():
    return "unanswered"

@app.route('/users/')
def user_list():
    return "all users"

@app.route('/users/<id>/')
def user_details(id):
    return "user details"

@app.route('/posts/<id>/vote/<int:value>/')
def vote(id, value):
    return "vote"

@app.route('/login/', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email', 'fullname', 'nickname'])
    return render_template('login.html', next = oid.get_next_url(), \
            error = oid.fetch_error())

@oid.after_login
def create_or_login(response):
    session['openid'] = response.identity_url
    try:
        user = User.objects.get(openid = response.identity_url)
        flash('Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    except:
        return redirect(url_for('create_profile', next = oid.get_next_url(), \
            name = response.fullname or response.nickname, \
            email = response.email))

@app.route('/create-profile/', methods = ['GET', 'POST'])
def create_profile():
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        if not name:
            flash(u'Error: you have to provide a name')
        elif not username:
            flash(u'Error: you must provide a username')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            new_user = User(username = username, name = name, email = email, openid = session['openid'])
            new_user.save()
            return redirect(oid.get_next_url())
    return render_template('create_profile.html', next_url=oid.get_next_url())

@app.route('/logout/')
def logout():
    session.pop('openid', None)
    flash('You were signed out')
    return redirect(oid.get_next_url())

if __name__ == '__main__':
    connect('flask-test')
    app.run()
