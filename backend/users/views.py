from django.contrib.auth import get_user_model
from djoser.permissions import CurrentUserOrAdmin
from djoser.views import UserViewSet
from recipes.serializers import SubscribeSerializer, SubscriptionsSerializer
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Subscription

User = get_user_model()


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


class SubscriptionsListView(ListModelMixin,
                            CreateModelMixin,
                            DestroyModelMixin,
                            GenericViewSet):
    queryset = Subscription.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'following_id'

    def list(self, request, *args, **kwargs):
        self.serializer_class = SubscriptionsSerializer
        self.queryset = User.objects.filter(
            following__user__follower__user=request.user).distinct()
        # self.queryset = [
        #     x.following for x in
        #     request.user.follower.all().select_related('following')
        # ]
        return super().list(request, args, kwargs)

    @action(['GET'], url_name='subscribe', detail=False)
    def create(self, request, *args, **kwargs):
        self.serializer_class = SubscribeSerializer
        return super().create(request, args, kwargs)

    @action(['DELETE'], url_name='subscribe', detail=False)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, args, kwargs)
