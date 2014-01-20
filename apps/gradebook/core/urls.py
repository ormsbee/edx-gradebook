from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from gradebook.core.rest import ContextDetail, ContextList
from gradebook.core.validators import EXTERNAL_ID_REGEX

urlpatterns = format_suffix_patterns(patterns('',
    url(
        r'^/contexts$',
        ContextList.as_view(),
        name='gradebook_context_list'
    ),
    url(
        '^/contexts/(?P<external_id>{})$'.format(EXTERNAL_ID_REGEX),
        ContextDetail.as_view(),
        name='gradebook_context_detail'
    ),
), allowed=['json', 'html'])
