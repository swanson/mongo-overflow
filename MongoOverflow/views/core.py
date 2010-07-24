from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

from backend.documents import Question

def index(request):
    return render_to_response('index.html', {'questions': Question.objects})

def question_details(request, qid):
    return render_to_response('details.html', \
                {'question': Question.objects.get(id = qid)})

