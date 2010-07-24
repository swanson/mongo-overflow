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
        html += "<a href='/questions/" + str(question.id) + "' >"
        html += '<li>'
        html += question.title + ' -- Asked by: ' + question.author.name
        html += ' -- %s Answer(s)' % (len(question.answers))
        html += '</li></a>'
    html += '</ul>'
    return HttpResponse(html)

def question_details(request, qid):
    question = Question.objects.get(id = qid)
    html = '<h1>%s</h1><ul>' % question.title
    for answer in question.answers:
        html += '<li>%s (Posted by %s) </li>' % (answer.body, answer.author.name)
    html += '</ul>'
    return HttpResponse(html)

