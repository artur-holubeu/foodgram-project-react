from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='check_recipes_in')
    is_in_shopping_cart = filters.BooleanFilter(method='check_recipes_in')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart', )

    def check_recipes_in(self, queryset, name, value):
        check_in_queryset = {
            'is_favorited': self.request.user.favorite_lists.all(),
            'is_in_shopping_cart': self.request.user.shopping_lists.all(),
        }
        if bool(value):
            favorite_id = [item.recipe.id for item
                           in check_in_queryset.get(name)]
            return queryset.filter(id__in=favorite_id)
        return queryset

