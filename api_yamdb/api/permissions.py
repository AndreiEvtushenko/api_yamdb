from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUserOrAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsUserOrForbidden(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.user.role == 'admin')


class SaveMethodsOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method not in SAFE_METHODS:
            if not request.user.is_authenticated:
                raise PermissionDenied('Нет прав доступа')
            if request.user.is_authenticated and request.user.role != 'admin':
                raise PermissionDenied('Нет прав доступа')
            else:
                return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method not in SAFE_METHODS:
            if not request.user.is_authenticated:
                raise PermissionDenied('Нет прав доступа')
            if request.user.is_authenticated and request.user.role != 'admin':
                raise PermissionDenied('Нет прав доступа')
            else:
                return True
