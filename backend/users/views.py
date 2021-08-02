from django.contrib.auth import get_user_model
from .pagination import UsersListPagination
from djoser.views import UserViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from djoser.permissions import CurrentUserOrAdmin


User = get_user_model()


class UsersView(UserViewSet):
    pagination_class = UsersListPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method in SAFE_METHODS:
            queryset = User.objects.all()
        return queryset

    @action(["get", "put", "patch", "delete"],
            detail=False,
            permission_classes=[CurrentUserOrAdmin]
            )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
