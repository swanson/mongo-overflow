from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

from backend.documents import Question, User, Answer, Comment
from datetime import datetime

def index(request):
    context = {
                'questions': Question.objects,
                'title': 'All Questions'
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
                        author = User.objects.get(name='matt'))
                new_comment.save()
                question.comments.append(new_comment)
                question.save()
                comment_form = Comment.Form()
        else:
            answer_form = Answer.Form(request.POST)
            if answer_form.is_valid():
                body = answer_form.cleaned_data['body']
                new_answer = Answer(body = body,
                        author = User.objects.get(name='matt'))
                new_answer.save()
                question.answers.append(new_answer)
                question.save()
                answer_form = Answer.Form()
    
    context = {
                'question': question,
                'title': Question.objects.get(id = qid).title,
                'comment_form': comment_form,
                'answer_form': answer_form,
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
            print tags
            new_question = Question(title = title, body = body, 
                    author = User.objects.get(name='matt'), 
                    tags = tags)
            new_question.save()
            return HttpResponseRedirect('/questions/%s' % new_question.id)
    else:
        form = Question.Form()
    context = {
            'title': 'Ask a New Question',
            'form': form,
        }
    return render_to_response('ask.html', context)
