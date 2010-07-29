from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from mongoengine.django.auth import MongoEngineBackend

from backend.documents import Question, User, Answer, Comment
from datetime import datetime
from django.contrib.auth import login as d_login
from django.contrib.auth import authenticate, logout
from django.utils import simplejson

def index(request):
    context = {
                'questions': Question.objects,
                'title': 'All Questions',
                'user':request.user
              }
    return render_to_response('index.html', context)

def question_details(request, qid):
    question = Question.objects.get(id = qid)
    answer_form = Answer.Form()
    comment_form = Comment.Form()
    if request.method == 'POST': #new answer submitted
        if 'comment_body' in request.POST:
            comment_form = Comment.Form(request.POST)
            if comment_form.is_valid():
                body = comment_form.cleaned_data['comment_body']
                new_comment = Comment(body = body, 
                        author = request.user)
                new_comment.save()
                question.comments.append(new_comment)
                question.save()
                comment_form = Comment.Form()
        else:
            answer_form = Answer.Form(request.POST)
            if answer_form.is_valid():
                body = answer_form.cleaned_data['body']
                new_answer = Answer(body = body,
                        author = request.user)
                new_answer.save()
                question.answers.append(new_answer)
                question.save()
                answer_form = Answer.Form()
        return HttpResponseRedirect('/questions/%s' % question.id)
    
    context = {
                'question': question,
                'title': Question.objects.get(id = qid).title,
                'comment_form': comment_form,
                'answer_form': answer_form,
                'user': request.user,
              }
    return render_to_response('details.html', context)

def unanswered(request):
    context = {
                'questions': Question.objects(answers__size = 0),
                'title': 'Unanswered Questions'
              }
    return render_to_response('index.html', context)

def add_question(request):
    if request.method == 'POST': #form was posted
        form = Question.Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            tags = form.cleaned_data['tags']
            if tags == '':
                tags = []
            else:
                tags = tags.split(',')
            new_question = Question(title = title, body = body, 
                    author = request.user,
                    tags = tags)
            new_question.save()
            return HttpResponseRedirect('/questions/%s' % new_question.id)
    else:
        form = Question.Form()
    context = {
            'title': 'Ask a New Question',
            'form': form,
            'user': request.user
        }
    return render_to_response('ask.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    user = None
    if request.method == 'POST':
        logout(request)
        username = request.POST['username']
        password = request.POST['password']
        foo = MongoEngineBackend()
        user = authenticate(username = username, password = password)
        if user is not None:
            d_login(request, user)
            return HttpResponseRedirect('/')
        else:
            #pseudo-register...
            new_user = User(username = username)
            new_user.set_password(password)
            new_user.save()
        form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    context = {
            'title': 'Log In',
            'form': form,
            'user': user,
        }
    return render_to_response('login.html', context)

def user_details(request, id):
    user = User.objects.get(id = id)
    context = {
                'user_to_show': user,
                'title': user.username,
                'user': request.user,
              }
    return render_to_response('user.html', context)

def user_list(request):
    context = {
                'users': User.objects,
                'title': 'All Users',
                'user': request.user,
              }
    return render_to_response('user_list.html', context)

def vote(request):
    results = {'success':False}
    if request.method == 'GET':
        GET = request.GET
        if GET.has_key('qid') and GET.has_key('vote'):
            qid = GET['qid']
            vote = GET['vote']
            question = Question.objects.get(id = qid)
            if vote == "up":
                question.vote_up(request.user)
            elif vote == "down":
                pass
            results = {'success':True}
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

