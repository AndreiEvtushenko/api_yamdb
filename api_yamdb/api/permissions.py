from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission


class SaveMethodsOrAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False


class UserViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.username in ['admin', ]:
            return True
        if request.user.role == 'admin':
            return True
        if request.method in ['GET', 'PATCH'] and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.username in ['admin', ]:
            return True
        if request.user.role == 'admin':
            return True
        if request.user == obj.user:
            return True
        return False


class CommentReviewsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role in ['admin', 'moderator']:
            return True
        if request.user.username in ['admin', 'moderator']:
            return True
        if request.method in SAFE_METHODS:
            return True
        if request.method not in SAFE_METHODS:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.username in ['admin', 'moderator']:
            return True
        if request.user.role in ['admin', 'moderator']:
            return True
        if request.user == obj.user:
            return True


class OnlyAdminOrSuperUserPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'admin' or
                request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin' or
                request.user.is_superuser)
