from django.contrib.auth import get_user_model
from djoser.permissions import CurrentUserOrAdmin
from djoser.views import UserViewSet
from recipes.pagination import ListLimitPagination
from recipes.serializers import (SubscribeSerializer, SubscriptionsSerializer,
                                 UnsubscribeSerializer)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Subscription

User = get_user_model()


class UsersView(UserViewSet):
    pagination_class = ListLimitPagination

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


class SubscriptionsListView(ListAPIView, GenericViewSet):
    queryset = Subscription.objects.get_queryset()
    serializer_class = SubscriptionsSerializer
    pagination_class = ListLimitPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        self.queryset = self.request.user.follower.all()
        return [user.following for user in self.queryset]


class SubscribeView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Subscription.objects.get_queryset()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'author_id'

    def destroy(self, request, *args, **kwargs):
        serializer = UnsubscribeSerializer(data={
            'user': request.user,
            'author_id': kwargs.get('author_id')
        })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
