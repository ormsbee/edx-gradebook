"""
This should have NO dependencies on any other app in the gradebook.

Signals:
* gradebook.submissions.created
* gradebook.submissions.accessed


"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django_extensions.db.fields import CreationDateTimeField, UUIDField


class Submission(models.Model):
    # Unique identifier that we can use elsewhere
    uuid = UUIDField(db_index=True)

    # Which attempt is this? Consecutive Submissions do not necessarily have
    # increasing attempt_num entries -- evaluation, re-scoring, etc. Some may
    # not have an attempt_num at all, as in the case for a class participation
    # grade.
    attempt_num = models.IntegerField(null=True)

    # submitted_at is separate from created_at to support re-scoring and other
    # processes that make new Submission objects relating to past user actions.
    submitted_at = CreationDateTimeField(db_index=True)
    created_at = CreationDateTimeField(db_index=True)


class SubmissionPart(models.Model):
    """
    Every Submission has one or more SubmissionParts
    """
    submission = models.ForeignKey(Submission)

    answer = models.TextField(blank=True, null=True)
    summary = models.CharField(max_length=255, db_index=True, blank=True, null=True)

    part_id = models.CharField(max_length=255)
    raw_score = models.FloatField(
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    unweighted_max_score = models.FloatField(null=True)
