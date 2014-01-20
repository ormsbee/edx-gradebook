"""
Define custom fields that we use in our gradebook.
"""
from django.db.models import CharField

from gradebook.core.validators import external_id_validator


class ExternalIDField(CharField):
    """
    Represent an ID from an external system. This ID is just a CharField with
    extra defaults (`max_length=255`, `db_index=True`, `unique=True`) and a
    validator that forces identifiers to be a combination of alphanumeric,
    dashes, underscores, and periods. We basically want to make sure it goes
    into a URL well. The only reason why periods are on that list is that edX
    course IDs have periods in them.

    These fields should be used at the edges, when clients are talking to our
    APIs and want to use their notion of IDs for students and contexts. Don't
    use these for our own storage and internal bookkeeping -- just use the
    primary key instead.
    """
    description = "Field for IDs that come from an external system."

    def __init__(self, *args, **kwargs):
        """
        Add defaults (`max_length=255`, `db_index=True`, `unique=True`) and our
        custom validator. Does not mutate `kwargs` (copies instead).
        """
        # Start with our defaults, then overwrite with kwargs values passed in
        new_kwargs = dict(max_length=255, db_index=True, unique=True)
        new_kwargs.update(kwargs)

        # Add custom validator
        new_kwargs["validators"] = new_kwargs.get("validators", []) + \
                                   [external_id_validator]

        super(ExternalIDField, self).__init__(*args, **new_kwargs)
