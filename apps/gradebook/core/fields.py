"""
Define custom fields that we use in our gradebook.
"""
from django.db.models import CharField

from gradebook.core.validators import external_id_validator


class ExternalIDField(CharField):
    """
    Represent an ID from an external system. This ID should be
    """
    description = "Field for IDs that come from an external system."

    def __init__(self, *args, **kwargs):
        defaults = {
            "max_length": 255,
            "db_index": True,
            "unique": True,
        }
        for key, val in defaults.items():
            kwargs[key] = kwargs.get(key, val)

        kwargs["validators"] = kwargs.get("validators", []) + [external_id_validator]

        super(CharField, self).__init__(*args, **kwargs)