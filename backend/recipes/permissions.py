from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if not isinstance(user := request.user, AnonymousUser):
            return user.is_staff
        return request.method in SAFE_METHODS


class ActiveCurrentUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if not isinstance(user := request.user, AnonymousUser):
            if (obj.author == user or user.is_staff) and user.is_active:
                return True
        return request.method in SAFE_METHODS
