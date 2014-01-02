from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from gradebook.core.rest import ContextDetail, ContextList

urlpatterns = format_suffix_patterns(patterns('',
    url(
        r'^/contexts$',
        ContextList.as_view(),
        name='gradebook_context_list'
    ),
    url(
        r'^/contexts/(?P<external_id>[\w\.\-\_]+)$',
        ContextDetail.as_view(),
        name='gradebook_context_detail'
    ),
), allowed=['json', 'html'])
