from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission, SAFE_METHODS


class SaveMethodsOrAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.role == 'admin':
                return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.role == 'admin':
                return True


class CommentReviewsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_authenticated:
            return True

        if request.user.is_authenticated:
            if (
                request.user.is_superuser or
                request.user.role in ['admin', 'moderator']
            ):
                return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if (
                request.user.is_superuser or
                request.user.role in ['admin', 'moderator']
            ):
                return True

            if (
                request.method in ['PATCH', 'DELETE'] and
                request.user == obj.author
            ):
                return True


class OnlyAdminOrSuperUserPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)

        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.role == 'admin':
                return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.role == 'admin':
                return True
