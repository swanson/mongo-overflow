from django.conf.urls.defaults import *
from views.core import index, add_question, unanswered, question_details

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     ('^$', index),
     ('^questions/$', index),
     ('^questions/ask/$', add_question),
     ('^questions/unanswered/$', unanswered),
     ('^questions/(?P<qid>[a-z0-9\-]+)/$', question_details),
)
urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'/home/matt/mongo-overflow/MongoOverflow/templates/', 'show_indexes': True}), )
