from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import FavoriteList, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import ActiveCurrentUserOrAdminOrReadOnly, AdminOrReadOnly
from .serializers import (FavoriteListSerializer, IngredientSerializers,
                          RecipeSerializers, ShoppingCartSerializer,
                          TagSerializers)
from .services import DownloadList


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
    search_fields = ('^name', )


class RecipeView(ModelViewSet):
    queryset = Recipe.objects.get_queryset()
    serializer_class = RecipeSerializers
    permission_classes = (ActiveCurrentUserOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.ingredients.all().delete()
        super().perform_destroy(instance)


class FavoriteView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'recipe_id'


class ShoppingCartView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'recipe_id'

    @action(['GET'], url_name='get_file', detail=False)
    def get_file(self, request, *args, **kwargs):
        queryset = request.user.shopping_lists.values_list(
            'recipe__ingredients__ingredient__name',
            'recipe__ingredients__ingredient__measurement_unit',
            'recipe__ingredients__amount'
        )
        return DownloadList(queryset).download_file()
