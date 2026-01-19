from rest_framework.exceptions import NotFound


class ObjectNotFound(NotFound):
    default_detail = "Not found."
    default_code = "NOT_FOUND"
