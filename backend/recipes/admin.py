from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import FavoriteList, Ingredient, Recipe, ShoppingCart, Tag


class FirstLetterListFilter(admin.SimpleListFilter):
    title = _('Первая буква (количество)')
    parameter_name = 'letter'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        lookups = []
        for letter in self._get_ru_letters():
            count = qs.filter(name__istartswith=letter).count()
            if count:
                lookups.append((letter, f'{letter} ({count})'))
        return lookups

    def queryset(self, request, queryset):
        filter_val = self.value()
        if filter_val:
            if filter_val in self._get_ru_letters():
                return queryset.filter(name__istartswith=self.value())
        return queryset

    @staticmethod
    def _get_ru_letters():
        lowercase = ''.join([chr(i) for i in range(ord('а'), ord('а') + 32)])
        uppercase = ''.join([chr(i) for i in range(ord('А'), ord('А') + 32)])
        return uppercase + lowercase


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug', )
    search_fields = ('id', 'name', 'slug', )
    list_filter = ('name', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    search_fields = ('id', 'name', )
    list_filter = (FirstLetterListFilter, )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author_name', )
    search_fields = ('id', 'name', )
    list_filter = ('name', 'author', 'tags', )
    readonly_fields = ('favorite_count', )

    def author_name(self, obj):
        return obj.author.username

    def favorite_count(self, obj):
        return obj.favorite_lists.count()

    author_name.short_description = _('Имя автора')
    favorite_count.short_description = _('Добавлено в избранное')


@admin.register(FavoriteList)
@admin.register(ShoppingCart)
class AuthorRecipesListAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'recipe_name', )
    list_filter = ('author', )

    def author_name(self, obj):
        return obj.author.username

    def recipe_name(self, obj):
        return obj.recipe.name

    author_name.short_description = _('Имя автора')
    recipe_name.short_description = _('Название рецепта')
