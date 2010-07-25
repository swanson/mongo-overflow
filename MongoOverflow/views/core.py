from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

from backend.documents import Question, User
from datetime import datetime

def index(request):
    return render_to_response('index.html', {'questions': Question.objects})

def question_details(request, qid):
    return render_to_response('details.html', \
                {'question': Question.objects.get(id = qid)})

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
    
    form = Question.Form()
    context = {
            'title': 'Ask a new question',
            'form': form,
        }
    return render_to_response('ask.html', context)
