"""
This file stitches together the URLs for all Gradebook apps. To include in a
project, insert the following line into your project's urls.py file:

    url(r'^api', include('gradebook.urls'))

That would cause all gradebook URLs to be included under /api
"""
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    # Core URLs: /contexts, /students
    url(r'^', include('gradebook.core.urls')),

    # Submissions URLs: /submissions
    url(r'^', include('gradebook.submissions.urls'))
)
