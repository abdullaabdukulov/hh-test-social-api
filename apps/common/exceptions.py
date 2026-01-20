from rest_framework.exceptions import NotFound, ValidationError


# Common
class ObjectNotFound(NotFound):
    default_detail = "Not found."
    default_code = "NOT_FOUND"


# users
class VerificationTokenInvalid(ValidationError):
    default_detail = "Invalid token."
    default_code = "VERIFICATION_TOKEN_INVALID"


class VerificationTokenUsed(ValidationError):
    default_detail = "Token already used."
    default_code = "VERIFICATION_TOKEN_USED"


class VerificationTokenExpired(ValidationError):
    default_detail = "Token expired."
    default_code = "VERIFICATION_TOKEN_EXPIRED"


# likes
class LikeAlreadyExists(ValidationError):
    default_detail = "You already liked this post."
    default_code = "LIKE_ALREADY_EXISTS"


class LikeNotFound(NotFound):
    default_detail = "Like not found."
    default_code = "LIKE_NOT_FOUND"


class CannotLikeOwnPost(ValidationError):
    default_detail = "You cannot like your own post."
    default_code = "CANNOT_LIKE_OWN_POST"


# posts
class PostNotFound(NotFound):
    default_detail = "Post not found."
    default_code = "POST_NOT_FOUND"
