from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from .models import Recipe


class IngredientFilter(SearchFilter):
    search_param = 'name'


class TagFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecipeFilter(filters.FilterSet):
    tags = TagFilter(field_name='tags__name', lookup_expr='in')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
