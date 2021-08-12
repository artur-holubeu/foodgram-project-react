from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import FavoriteList, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import ActiveCurrentUserOrAdminOrReadOnly, AdminOrReadOnly
from .serializers import (FavoriteListSerializer, IngredientSerializers,
                          RecipeSerializers, ShoppingCartSerializer,
                          TagSerializers)


class TagView(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    pagination_class = None
    permission_classes = (AdminOrReadOnly, )


class IngredientView(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    pagination_class = None
    permission_classes = (AdminOrReadOnly, )
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', '@name', )


class RecipeView(ModelViewSet):
    queryset = Recipe.objects.get_queryset()
    serializer_class = RecipeSerializers
    permission_classes = (ActiveCurrentUserOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter


class FavoriteView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = FavoriteList.objects.get_queryset()
    serializer_class = FavoriteListSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'recipe_id'


class ShoppingCartView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ShoppingCart.objects.get_queryset()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'recipe_id'


# @action(methods=['get'], detail=False, permisson_class=IsAuthenticated)
# def download_shopping_cart(request):
#     x = request
#     user = request.user
#     print(user)
