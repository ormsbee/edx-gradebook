.. WARNING::
   There is nothing remotely producation ready here. Development has only just
   started, and anyting can change at any time.

Overview
########

The goal of edx-gradebook is to provide an API that accepts scored submissions
of student work and generates computed course grade information at the
individual and class levels. The gradebook will allow for manual grade entry
as well as batch uploads for those courses that require specialized grading
rules that are beyond the scope of this project.

Install and Run
###############

Install::

  pip install -r requirements/dev.txt

Run tests::

  python sample_project/manage.py test

Run server::

  python sample_project/manage.py runserver_plus

Directories
###########


`docs`
  Sphinx docs directory.

`apps/gradebook`
  Holds all apps relating to the gradebook. Most code lives here.

`requirements`
  Requirements files, with `common.txt` being the minimum needed to run the
  server, and `dev.txt` what developers need to install.

`sample_project`
  Project that exists only to have a shell to put our gradebook apps into.

Architectural Goals
###################

1. Accomodate course sizes in the hundreds of thousands.
2. Simple setup. At baseline, it should work with a standard RDBMS. Extra server
   dependencies may be added to enable certain features or for high performance.
3. Allow edx-gradebook apps to be embedded directly into another project, or
   used as a RESTful service.
4. Do not tie to XBlock or hierarchical course structure.
5. Do not have edx-platform as a dependency.
6. At any given time, we should have all the information necessary to compute a
   student's grade within edx-gradebook. Asking for a student's grade should not
   cause us to have to instantiate and execute XBlock code, or reach out to a
   third party service.
7. Allow for auditing. This means both that grade accesses should be logged, and
   that wherever possible records should be appended to and not mutated. It
   doesn't need to be cheap, but we should be able to reconstruct the state of
   the world for any given time.
8. Allow for individual gradebook apps to be swapped out. This is for both for
   scalability and customization reasons.

App Conventions
###############

With the exception of `gradebook.core`, app models should not be directly
accessed from other apps. Apps should emit signals when they have things that
are of interest to other apps. Apps should also specify an `api.py` file that
contains the extent of their public interface. This interface should only return
simple serializable types — basically anything that can be sent over JSON.
Namedtuples are also allowed, since they are trivial to convert. The REST API
published by the app should only expose functionality that can be found in
`api.py`.

`gradebook.core`
  The absolute basic pieces, representing contexts (courses) and students.

`gradebook.submissions`
  Handles raw submission (user X for course Y, problem Z got 1.0 points at this
  time) creation, storage, and querying. Creation should be very fast. Lookup
  can be slightly more expensive.

  Dependency: `core`.

`gradebook.raw_scores`
  Listens to submissions and maintains raw (unweighted) score information.
  Lookup for all scores for a given student for a given context and student
  should be very fast.

  Dependency: `submissions`

`gradebook.gradecalc`
  Maintains grading policies and queries `raw_scores` for information it needs.

  Dependency: `raw_scores`

TODO: Haven't really figured where auditing, permissions, and batch
import/export will go.

