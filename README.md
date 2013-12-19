edx-gradebook
=============

Apps
----

gradebook.core = Context, Student
gradebook.submissions = Submission (dependency: core)
gradebook.raw_scores = RawScore (dependency: submissions)
gradebook.policies (dependency: core)
gradebook.gradecalc (raw_scores + policies)
gradebook.batch.import
                export

gradebook.audit (dependency: core?)


gradebook.permissions <- might be part of core


/contexts
/students
/submissions
/raw_scores
/grades
/policies
/downloads
/uploads

/students/811079b4-90ad-49da-935a-d93feadf7581

    {
        "contexts" : {
            "811079b4-90ad-49da-935a-d93feadf7581" : {
                "submissions" : "/api/submissions?student=811079b4-90ad-49da-935a-d93feadf7581&context=811079b4-90ad-49da-935a-d93feadf7581"
            },
        }
    }

A suggestion from interwebs:

either modify manage.py and wsgi.py for signal setup or

signals = signals.py
listeners = listeners.py

start_listening() invoked from models.py

Conventions
-- UUID for external world things
-- slugs?


Each Django app will have the following conventions:

/lib - non-Django code
/management/commands/

/migrations - South Migrations
/static
/templates
/templatetags
/tests

admin.py
api.py
context_processors.py
feeds.py
forms.py
middleware.py
models.py
rest.py
serializers.py
signals.py
sitemaps.py
startup.py
urls.py
validators.py
views.py