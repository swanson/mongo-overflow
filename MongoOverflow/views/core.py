from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

from backend.documents import Question

def index(request):
    questions = Question.objects
    html = """<h1>Welcome to MongoOverflow</h1>
                It's like StackOverflow, but worse!
                <ul>"""
    for question in questions:
        html += '<li>'
        html += question.title + ' -- Asked by: ' + question.author.name
        html += ' -- %s Answer(s)' % (len(question.answers))
        html += '</li>'
    html += '</ul>'
    return HttpResponse(html)

