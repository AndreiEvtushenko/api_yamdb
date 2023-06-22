from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import SAFE_METHODS, BasePermission


class SaveMethodsOrAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                return True

        return False


class CommentReviewsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        if request.user.is_authenticated:
            if request.user.role in ['admin', 'moderator']:
                return True
            if request.method == 'POST':
                return True
        if request.method in SAFE_METHODS:
            return True
        if request.method not in SAFE_METHODS:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.role in ['admin', 'moderator']:
                return True
            if request.method in ['PATCH', 'DELETE'] and request.user == obj.author:
                return True


class OnlyAdminOrSuperUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        if request.user.is_authenticated:

            if request.user.is_superuser:
                return True
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                return True
