# edx-gradebook API

The goal of edx-gradebook is to provide an API that accepts scored submissions
of student work and generates computed course grade information at the
individual and class levels. The gradebook will allow for manual grade entry
as well as batch uploads for those courses that require specialized grading
rules that are beyond the scope of this project.

## Technical Design Goals

Based on lessons learned with our existing system:

1. At any given time, we should have all the information necessary to compute a
student's grade within edx-gradebook. Asking for a student's grade should not
cause us to have to instantiate and execute XBlock code, or reach out to a third
party service.
2. It should be possible to deploy edx-gradebook separately from edx-platform.
3. Scoring should not be explicitly tied to XBlocks or hierarchical course
structure.
4. It should be possible to batch import and export scores.
5. Any manipulation of student score should be clearly traceable for auditing
purposes.

## Submission

Any time an answer and/or score for an item is sent to edx-gradebook, a new
Submission is created. Submissions are immutable.

A few notes:

1. A problem may have multiple parts. A submission should capture the state of
all of those parts. When people submit, they are submitting the entire problem
for grading.
2. This does not currently cover a bulk submission of multiple problems at the
same time, though we should for the purposes of people being able to upload
grades for their courses.
3. There is other information *about* a submission or group of submissions
(like student feedback, staff-only comments), that are separate from the
submissions themselves.
4. We don't have to implement it all at once, and there are undoubtedly other
submission types that aren't covered here. The hope is just that this sketch is
enough of a framework to build around.

### Creating a Submission

`POST /submission`

Required Fields:

* `type`:
    * `student`: Normal submission that edx-gradebook receives from edx-platform
                 when a student submits a problem.
    * `amendment`: Launched by an automated process (e.g. re-scoring), this
                   submission will reference a previous submission and add
                   corrective information. It does not alter the original
                   submission. We would use these to recover from situations
                   where the problem or problem evaluation code had bugs.
    * `evaluation`: Teaching staff add scoring information to an existing
                    Student submission. Again, this Submission references the
                    original and does not modify it.
    * `manual_entry`: Teaching staff create an entirely new submission for
                      something like a student's participation grade.
* `contexts`: Typically course identifiers, but content in a shared module used
              by a course might send context identifiers for both the shared
              module and the course. You can use `context` if you only have one
              context (this is equivalent to having `contexts` as a list with
              one context in it).
* `students`: Identifiers for one or more students that the submission is
              associated with. Two students might work together on a group
              project submitted in both their names. You can use `student` if
              you only have one student (this is equivalent to having `students`
              as a list with one student in it).
* `item`: This should uniquely identify a graded item within a given context.

Optional Fields:

* `raw_scores`: Dictionary mapping problem part identifiers to raw scores. Raw
                scores are decimal values between 0.0 and 1.0. Problem weighting
                happens separately as a policy setting. If you have only one
                problem part, you can use `raw_score`, which will be equivalent
                to having a `raw_scores` with one problem part named `default`.
                This is optional because Students might submit something that
                requires manual evaluation, or partial manual evaluation. Raw
                scores can be `null` to indicate that no score has been assigned
                (i.e. it requires manual scoring). Always send entries for all
                problem parts.
* `answers`: Dictionary mapping problem part identifiers to answers. Answers are
             text blobs. It should be possible for whatever is submitting the
             problem to reconstruct the state of the user submission based on
             this field. It does not necessarily have to be the state in its
             entirety (e.g. it could be an S3 bucket address). If you have only
             one problem part, you can use `answer`, which will be equivalent
             to having `answers` with one problem part named `default`. This is
             required for a Student submission. Answers can be `null` to
             indicate that the user has not entered anything for that part of
             the problem. Always send entries for all problem parts.
* `summaries`: Dictionary mapping problem part identifiers to short (< 256 byte)
               strings that can be used to classify answers. This would allow us
               to easily generate histograms for answers to certain types of
               questions. `summary` may be used as a convenience if there is
               only one problem part.
* `version`: The version of the item being submitted against.
* `variant`: Usually a per-student variable, for a dynamic item, this would tell
             us what variant of the problem the student saw. This would be a
             random seed in edx-platform, but could be explicitly named as well.
* `submitted_at`: Defaults to now, but can be explicitly if it's being done by
                  an async process. For instance, say a student submitted their
                  answer to a simluator that took two hours to evaluate it. We
                  want to make sure that when the results of that come to us,
                  we are capturing the student submission time and not the
                  evaluation time. A separate `created_at` will automatically
                  be created for every submission. All times are UTC.
* `attempt_number`: Number representing which attempt this was for the student.
                    This would automatically increment for student submissions,
                    but it could also be set explicitly in case it's necessary
                    to adjust during recovery from bugs in grading or problem
                    code.
* `meta`: Dictionary of arbitrary values (can have sub-dictionaries) that the
          submitting application can annotate this submission with. As an
          example, a re-scoring run might specify what user triggered the
          re-scoring, and what task ID the process doing the re-scoring was for
          auditing purposes.

Example:

<pre>
{
    "type": "student",
    "contexts" : ["edu.mit.eecs.6002x.2014.spring"],
    "students" : [
        "811079b4-90ad-49da-935a-d93feadf7581",
        "f76ec2ae-dcf4-40a1-a3cb-5951b225b129"
    ],
    "item": "i4x://edX/DemoX/problem/75f9562c77bc4858b61f907bb810d974",
    "answers" : {
        "a" : "blue",
        "b" : "cat",
        "c" : ["pie", "cake"]
    },
    "version" : "20131100_2301",
    "variant" : "1",
    "submitted_at" : "2013-04-02 11:00:42",
    "attempt_number" : 2,
    "hint_shown" : {
        "a" : true,
        "b" : false,
        "c" : false
    },
    "raw_scores" : {
        "a" : 1.0,
        "b" : 0.0,
        "c" : 0.5
    }
}
</pre>

### Concerns

1. Simultaneously supporting human grading and automatic grading adds complexity
   to the system.
2. The design assumes items are usages, but should they also capture definition
   IDs as well?
3. Submissions would be part of SubmissionHistories, where a SubmissionHistory
   is a (course, user, context, item) tuple. Should that be more explicit
   somehow?
4. Is supporting multiple contexts for a given submission something that would
   actually be useful?
5. What kind of support do we need for hints? Punting on this for now. Is it
   just boolean for whether hints are or aren't present? Different levels of
   hints? Because we intend to keep a separate tracking of the highest and most
   recent scores for a given problem part, penalization for hints gets messy.
   Might address this by simply saying that grading by "highest score achieved"
   and penalization for hints are incompatible with each other and cannot be
   used on the same problem.
