from django.conf.urls.defaults import *
from views.core import (index, add_question, unanswered, 
        question_details, login_view, logout_view, user_details,
        user_list, vote)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     ('^$', index),
     ('^login/$', login_view),
     ('^logout/$', logout_view),
     ('^questions/$', index),
     ('^questions/ask/$', add_question),
     ('^questions/unanswered/$', unanswered),
     ('^questions/(?P<qid>[a-z0-9\-]+)/$', question_details),
     ('^users/$', user_list),
     ('^users/(?P<id>[a-z0-9\-]+)/$', user_details),
     ('^vote/$', vote),
)
urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'/home/matt/mongo-overflow/MongoOverflow/templates/', 'show_indexes': True}), )
