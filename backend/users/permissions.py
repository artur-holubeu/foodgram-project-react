from rest_framework.permissions import SAFE_METHODS, BasePermission


class CurrentUserOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if type(obj) == type(user) and obj == user or user.is_staff:
                return True
        return request.method in SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
