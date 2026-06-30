import re

NULL_VALUES = {
    "", " ", "na", "n/a", "null", "none", "-", "--"
}

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

E164_REGEX = re.compile(
    r"^\+[1-9]\d{1,14}$"
)

TITLE_MAP = {
    "swe": "Software Engineer",
    "dev" : "Development",
    "sde": "Software Development Engineer",
    "devops": "DevOps"
}