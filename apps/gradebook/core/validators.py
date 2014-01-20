import re

from django.core.exceptions import ValidationError

# Note that we intentionally do not use \w, because we don't want to allow
# various unicode characters. This is a separate constant so we can use it for
# our urls.py
EXTERNAL_ID_REGEX = r'^[a-zA-Z0-9_\-\.]+$'

def external_id_validator(value):
    """
    Check that it's a valid external ID: alphanum, dashes, underscores, periods.
    Not using RegexValidator because that doesn't let you dynamically include
    the bad value in the error message.
    """
    if not re.match(EXTERNAL_ID_REGEX, value):
        raise ValidationError(
            u"{} is not a valid external ID. ".format(value) +
            u"Must only use letters, numbers, dashes, underscores, and periods."
        )
