from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsVerifiedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_verified)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and obj.author_id == request.user.id
        )
