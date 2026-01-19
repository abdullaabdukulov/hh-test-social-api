from django.core.validators import RegexValidator

username_validator = RegexValidator(
    r"^[a-zA-Z0-9_]{3,32}$",
    (
        "Username must be 3–32 characters long and contain only letters, "
        "numbers, or underscores."
    ),
)

full_name_validator = RegexValidator(
    r"^[A-Za-zА-Яа-яЁё\s\-]{2,100}$",
    (
        "Full name must be 2–100 characters and may contain only letters "
        "(Latin/Cyrillic), spaces, and hyphens."
    ),
)
