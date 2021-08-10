from django.contrib import admin

from .models import FavoriteList, Ingredient, Recipe, ShoppingCart, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug', )
    search_fields = ('id', 'name', 'slug', )
    list_filter = ('name', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    search_fields = ('id', 'name', )
    list_filter = ('name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author_name', )
    search_fields = ('id', 'name', )
    list_filter = ('name', 'author', 'tags')

    def author_name(self, obj):
        return obj.author.name


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'recipe_name')
    list_filter = ('author',)

    def author_name(self, obj):
        return obj.author.name

    def recipe_name(self, obj):
        return obj.recipe.name


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'recipe_name')
    list_filter = ('author',)

    def author_name(self, obj):
        return obj.author.name

    def recipe_name(self, obj):
        return obj.recipe.name
