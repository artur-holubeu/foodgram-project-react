from rest_framework.permissions import (
    SAFE_METHODS, BasePermission, IsAuthenticatedOrReadOnly,
)


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                return True
        return request.method in SAFE_METHODS


class ActiveCurrentUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if (obj.author == user or user.is_staff) and user.is_active:
                return True
        return request.method in SAFE_METHODS
