from django.contrib.auth import get_user_model
from djoser.permissions import CurrentUserOrAdmin
from djoser.views import UserViewSet
from recipes.serializers import SubscriptionsSerializer
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Subscription


class UsersView(UserViewSet):

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return get_user_model().objects.all()
        return super().get_queryset()

    @action(["get", "put", "patch", "delete"],
            detail=False,
            permission_classes=[CurrentUserOrAdmin]
            )
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)


class SubscriptionsListView(ListAPIView,
                            CreateModelMixin,
                            DestroyModelMixin,
                            GenericViewSet):
    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'following_id'

    def get_queryset(self):
        if self.action == 'list':
            return [
                x.following for x in
                self.request.user.follower.all().select_related('following')
            ]
        if self.action == 'destroy':
            return self.request.user.follower
        return Subscription.objects.all()

    @action(['GET'], url_name='subscribe', detail=False)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @action(['DELETE'], url_name='subscribe', detail=False)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, args, kwargs)
