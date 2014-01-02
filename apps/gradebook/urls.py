"""
This file stitches together the URLs for all Gradebook apps. To include in a
project, insert the following line into your project's urls.py file:

    url(r'^api', include('gradebook.urls'))

That would cause all gradebook URLs to be included under /api

TODO: Make it so that it exposes both an /api and a web interface under a
      different directory.

Random consideration: If we really do get to a point where there are swappable
                      apps, we could make a method that spits out a urlpatterns
                      based on app names that are passed in. o.O
"""
from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    # Core URLs: /contexts, /students
    url(r'^', include('gradebook.core.urls')),

    # Submissions URLs: /submissions
    url(r'^', include('gradebook.submissions.urls'))
)
