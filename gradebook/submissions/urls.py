from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from gradebook.submissions.rest import SubmissionList

urlpatterns = format_suffix_patterns(patterns('',
    url(
        r'^/submissions$',
        SubmissionList.as_view(),
        name='gradebook_submissions'
    ),

#    # Contexts
#    url(
#        r'^contexts/$',
#        views.ContextList.as_view(),
#        name='context-list'
#    ),
#    url(
#        r'^contexts/(?P<pk>[0-9]+)$',
#        views.ContextDetail.as_view(),
#        name='context-detail'
#    ),
#
#    # Answer list. This is less a useful API piece to have, and more a simple
#    # way for me to play with the REST lib we're using.
#    url(
#        r'^answers/$',
#        views.AnswerList.as_view(),
#        name='answer-list'
#    ),
#    url(
#        r'^answers/(?P<pk>[0-9]+)$',
#        views.AnswerDetail.as_view(),
#        name='answer-detail'
#    )
), allowed=['json', 'html'])
