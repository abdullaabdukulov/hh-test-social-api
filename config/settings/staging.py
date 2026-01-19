from .base import *  # noqa

ALLOWED_HOSTS = []
DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "[Bearer {JWT}]": {
            "name": "Authorization",
            "type": "apiKey",
            "in": "header",
        }
    },
    "USE_SESSION_AUTH": False,
    "SUPPORTED_SUBMIT_METHODS": ["get", "post", "put", "delete", "patch"],
}
