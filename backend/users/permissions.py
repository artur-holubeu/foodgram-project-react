from rest_framework.permissions import SAFE_METHODS, BasePermission
from django.contrib.auth.models import AnonymousUser


class CurrentUserOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if not isinstance(user := request.user, AnonymousUser):
            if type(obj) == type(user) and obj == user or user.is_staff:
                return True
        return request.method in SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
