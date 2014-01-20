from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from gradebook.core.urls import EXTERNAL_ID_REGEX
from gradebook.submissions.rest import SubmissionList

urlpatterns = format_suffix_patterns(patterns('',
    url(
        r'^/submissions$',
        SubmissionList.as_view(),
        name='gradebook_submissions'
    ),

), allowed=['json', 'html'])
