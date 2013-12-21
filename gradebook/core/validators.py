from django.core.validators import RegexValidator

external_id_validator = RegexValidator(
    r'^[\w\.\-\_]+$',
    message="External IDs can only have letters, numbers, dashes, underscores, "
            "and periods."
)