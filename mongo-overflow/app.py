from flask import Flask, g, session, request, render_template, flash, redirect, url_for, jsonify
from flaskext.openid import OpenID
from db.documents import User, Question, Answer, Comment, Vote, AnswerVote, map_reduce_tags
from db.forms import QuestionForm, AnswerForm, CommentForm
from mongoengine import *
from datetime import datetime
import json


app = Flask(__name__)
app.debug = True
app.secret_key = 'very_secret_key'
oid = OpenID(app)

@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.now()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

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
    return render_template('index.html', questions = Question.objects, title = 'All Questions')

@app.route('/questions/<id>/', methods = ['GET'])
def question_details(id):
    question = Question.objects.get(id = id)
    answer_form = AnswerForm()
    comment_form = CommentForm()
    your_vote = 0
    answer_votes = []
    if g.user:
        try:
            vote = Vote.objects.get(user=g.user, question=question)
            your_vote = vote.score
        except:
            pass
        try:
            answer_votes = AnswerVote.objects(user=g.user, answer__in=question.answers)
        except:
            pass
    return render_template('details.html', question = question, 
                                            title = question.title,
                                            answer_form = answer_form,
                                            comment_form = comment_form,
                                            your_vote = your_vote,
                                            answer_votes = answer_votes)

@app.route('/questions/ask/', methods=['POST', 'GET'])
def ask_question():
    form = QuestionForm(request.form)
    if request.method == 'POST' and form.validate() and g.user:
        title = form.title.data
        body = form.body.data
        tags = form.tags.data
        if tags == '':
            tags = []
        else:
            tags = tags.split(',')
            tags = [tag.strip() for tag in tags]
        new_question = Question(title = title, body = body, 
                    author = g.user,
                    tags = tags)
        new_question.save()
        return redirect('/questions/%s' % new_question.id)
    elif not g.user:
        flash("Please login")
    elif request.method == 'POST':
        flash("Put it some data please")

    return render_template('ask.html', form = form, title = 'Ask a question')

@app.route('/tags/')
def get_tags():
    return render_template('tags.html', title = 'Tags', tags = map_reduce_tags())
    

@app.route('/questions/unanswered/')
def unanswered_questions():
    return render_template('index.html', questions = Question.objects(answers__size = 0), 
                                        title = 'Unanswered Questions')

@app.route('/questions/tagged/<tag>/')
def questions_by_tag(tag):
    return render_template('index.html', title = 'Questions tagged with "%s"' % tag, 
                                        questions = Question.objects(tags__contains=tag))

@app.route('/users/')
def user_list():
    return render_template('user_list.html', title = 'All Users', users = User.objects)

@app.route('/users/<id>/')
def user_details(id):
    user = User.objects.get(id = id)
    return render_template('user.html', title = "%s's Profile" % user.username, 
                                        user = user)

@app.route('/posts/question/<id>/comment/', methods = ['POST'])
def add_comment_to_question(id):
    comment_form = CommentForm(request.form)
    if g.user and comment_form.validate():
        question = Question.objects.get(id = id)
        new_comment = Comment(body = comment_form.comment_body.data, author = g.user)
        new_comment.save()
        question.comments.append(new_comment)
        question.save()
        return redirect('/questions/%s' % id) #avoid double POSTs
    else:
        #add error handling
        return redirect('/questions/%s' % id) #avoid double POSTs

@app.route('/posts/question/<id>/answer/', methods = ['POST'])
def add_answer_to_question(id):
    answer_form = AnswerForm(request.form)
    if g.user and answer_form.validate():
        question = Question.objects.get(id = id)
        new_answer = Answer(body = answer_form.answer_body.data, author = g.user)
        new_answer.save()
        question.answers.append(new_answer)
        question.save()
        return redirect('/questions/%s' % id) #avoid double POSTs
    else:
        #add error handling
        return redirect('/questions/%s' % id) #avoid double POSTs

@app.route('/posts/question/<id>/answer/<answer_id>/comment/', methods = ['POST'])
def add_comment_to_answer(id, answer_id):
    comment_form = CommentForm(request.form)
    if g.user and comment_form.validate():
        answer = Answer.objects.get(id = answer_id)
        new_comment = Comment(body = comment_form.comment_body.data, author = g.user)
        new_comment.save()
        answer.comments.append(new_comment)
        answer.save()
        return redirect('/questions/%s' % id) #avoid double POSTs
    else:
        #add error handling
        return redirect('/questions/%s' % id) #avoid double POSTs


@app.route('/posts/question/<id>/vote/<int:value>/', methods = ['POST'])
def vote_on_question(id, value):
    if g.user:
        question = Question.objects.get(id = id)
        if question.author == g.user:
            return jsonify(success = False, msg = "You can't vote on your own question")
        if value is 1:
            v = question.vote_up(g.user)
        elif value is 2:
            v = question.vote_down(g.user)
        question.reload()
        return jsonify(success = True, count = question.score, vote = v)
    return jsonify(success = False)

@app.route('/posts/answer/<id>/vote/<int:value>/', methods = ['POST'])
def vote_on_answer(id, value):
    if g.user:
        answer = Answer.objects.get(id = id)
        if answer.author == g.user:
            return jsonify(success = False, msg = "You can't vote on your own answer")
        if value is 1:
            v = answer.vote_up(g.user)
        elif value is 2:
            v = answer.vote_down(g.user)
        answer.reload()
        return jsonify(success = True, count = answer.score, vote = v)
    return jsonify(success = False)


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
        user.last_login = datetime.now()
        user.save()
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
            new_user = User(username = username, name = name, email = email, \
                    openid = session['openid'], joined = datetime.now(), \
                    last_login = datetime.now())
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
    app.run(host='0.0.0.0', port=8000)
