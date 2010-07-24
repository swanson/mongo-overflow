from django.conf.urls.defaults import *
from views.core import index, question_details

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     ('^$', index),
     ('^questions/$', index),
     ('^questions/(?P<qid>[a-z0-9\-]+)/$', question_details),
)
