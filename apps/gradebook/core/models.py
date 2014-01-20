"""
These models are meant to be used by any application, and can be linked to with
a foreign key relation.
"""
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from gradebook.core.fields import ExternalIDField


class Organization(models.Model):
    """
    An Organization
    """


class Context(models.Model):
    """
    A Context is an identifier used to group content. A Context could be a
    course, but it could be a smaller collection of course content as well.
    Items can be associated with multiple Contexts. The purpose of a Context
    is mostly to be able to quickly constrain a search so that we can pull back
    all the student's data that is relevant for whatever course they're looking
    at.

    Contexts are created and updated, but should never be deleted. This is
    particularly important because data and processes downstream may depend on
    a given Context.
    """
    external_id = ExternalIDField("External ID")
    name = models.CharField("Name", max_length=255, db_index=True)
    description = models.TextField("Description", blank=True)
    created_at = CreationDateTimeField(db_index=True)
    updated_at = ModificationDateTimeField(db_index=True)


class Student(models.Model):
    """

    """
    external_id = ExternalIDField("External ID")
    created_at = CreationDateTimeField(db_index=True)
    updated_at = ModificationDateTimeField(db_index=True)
