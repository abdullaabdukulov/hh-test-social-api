from django.core.validators import RegexValidator

username_validator = RegexValidator(
    r"^[a-zA-Z0-9_]{3,32}$",
    (
        "Username must be 3–32 characters long and contain only letters, "
        "numbers, or underscores."
    ),
)
