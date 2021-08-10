from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import FavoriteList, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import ListLimitPagination
from .permissions import ActiveCurrentUserOrAdminOrReadOnly, AdminOrReadOnly
from .serializers import (FavoriteListSerializer, IngredientSerializers,
                          RecipeSerializers, ShoppingCartSerializer,
                          TagSerializers)


class TagView(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    pagination_class = None
    permission_classes = (AdminOrReadOnly,)


class IngredientView(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    pagination_class = None
    permission_classes = (AdminOrReadOnly, )
    filter_backends = (IngredientFilter,)
    search_fields = ('^name', )


class RecipeView(ModelViewSet):
    queryset = Recipe.objects.get_queryset()
    serializer_class = RecipeSerializers
    pagination_class = ListLimitPagination
    permission_classes = (ActiveCurrentUserOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_queryset(self):
        if self.request.query_params.get('is_favorited', False) == 'true':
            favorite_id = [user.recipe.id for user
                           in self.request.user.favorite_lists.all()]
            return self.queryset.filter(id__in=favorite_id)
        if self.request.query_params.get(
                'is_in_shopping_cart', False) == 'true':
            shopping_cart_id = [user.recipe.id for user
                                in self.request.user.shopping_lists.all()]
            return self.queryset.filter(id__in=shopping_cart_id)
        return super().get_queryset()


class FavoriteView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = FavoriteList.objects.get_queryset()
    serializer_class = FavoriteListSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe_id'


class ShoppingCartView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ShoppingCart.objects.get_queryset()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe_id'


# @action(methods=['get'], detail=False, permisson_class=IsAuthenticated)
# def download_shopping_cart(request):
#     x = request
#     user = request.user
#     print(user)


# class FavoriteListView(ListModelMixin, GenericViewSet):
#     queryset = FavoriteList.objects.get_queryset()
#     serializer_class = FavoriteListSerializer
#     pagination_class = ListLimitPagination
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         self.queryset = self.request.user.favorite_lists.all()
#         return [user.recipe for user in self.queryset]

# class ShoppingCartView(ListModelMixin, GenericViewSet):
#     queryset = ShoppingCart.objects.get_queryset()
#     serializer_class = ShoppingCartSerializer
#     pagination_class = ListLimitPagination
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         self.queryset = self.request.user.shopping_lists.all()
#         return [user.recipe for user in self.queryset]
