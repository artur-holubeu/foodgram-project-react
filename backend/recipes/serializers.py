from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import Subscription
from users.serializers import UserBaseSerializer

from .models import (FavoriteList, Ingredient, IngredientsAmount, Recipe,
                     ShoppingCart, Tag)

User = get_user_model()


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientAmountSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'amount')


class RecipeSerializers(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientAmountSerializers(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['tags'] = [TagSerializers(x).data for x in instance.tags.all()]

        rep['ingredients'] = [{
            **IngredientSerializers(x.ingredient).data,
            **{'amount': x.amount}
        } for x in instance.ingredients.all().select_related('ingredient')]

        user = self.context['request'].user
        if user.is_anonymous:
            rep['is_favorited'] = False
            rep['is_in_shopping_cart'] = False
        else:
            rep['is_favorited'] = instance.favorite_lists.filter(
                author=user).exists()
            rep['is_in_shopping_cart'] = instance.shopping_lists.filter(
                author=user).exists()

        return rep

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        ingredients = [
            IngredientsAmount.objects.create(
                ingredient=x.get('id'),
                amount=x.get('amount'),
            ) for x in ingredients]
        recipe.tags.add(*tags)
        recipe.ingredients.add(*ingredients)
        return recipe

    def update(self, instance, validated_data):
        self._update_ingredients()
        self._update_tags()
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.save()
        return instance

    def _update_ingredients(self):
        new_data_raw = self.validated_data.get('ingredients')
        if new_data_raw:
            self.instance.ingredients.all().delete()
            ingredients = [
                IngredientsAmount.objects.create(
                    ingredient=x.get('id'),
                    amount=x.get('amount'),
                ) for x in new_data_raw]
            self.instance.ingredients.add(*ingredients)

    def _update_tags(self):
        new_data_raw = self.validated_data.get('tags')
        if new_data_raw:
            self.instance.tags.clear()
            self.instance.tags.add(*self.validated_data['tags'])


class RecipeShortSerializers(RecipeSerializers):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)

    def to_representation(self, instance):
        rep = dict()
        for x in self.fields:
            rep[x] = instance.__dict__.get(x)
        return rep


class SubscriptionsSerializer(UserBaseSerializer):
    recipes = RecipeShortSerializers(many=True, read_only=True)

    class Meta(UserBaseSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',)

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep['recipes_count'] = len(rep['recipes'])
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit')
        if recipes_limit:
            rep['recipes'] = rep['recipes'][:int(recipes_limit)]
        return rep

    def validate(self, data):
        request = self.context['request']
        following = get_object_or_404(
            User,
            pk=request.parser_context['kwargs'].get('following_id')
        )
        user = request.user

        if following.id == user.id:
            raise serializers.ValidationError({
                'errors': ('Пользователь не может быть подписан '
                           'на самого себя.'),
            })

        if Subscription.objects.filter(
                user=user, following=following).exists():
            raise serializers.ValidationError({
                'errors': 'Пользователь уже подписан на этого автора.',
            })

        if recipes_limit := self.context['request'].query_params.get(
                'recipes_limit'):

            if int(recipes_limit) < 0:
                raise serializers.ValidationError({
                    'errors': ('Минимальное количество рецептов не может '
                               'быть меньше нуля.'),
                })
        return {
            'user': user,
            'following': following
        }

    def create(self, validated_data):
        return Subscription.objects.create(
            user=validated_data['user'],
            following=validated_data['following']
        ).following


class FavoriteListSerializer(serializers.ModelSerializer):
    recipe = RecipeShortSerializers(read_only=True)

    class Meta:
        model = FavoriteList
        fields = ('recipe', )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep['recipe']

    def validate(self, attrs):
        request = self.context['request']
        recipe = get_object_or_404(
            Recipe,
            pk=request.parser_context['kwargs'].get('recipe_id')
        )
        author = request.user

        if FavoriteList.objects.filter(
                author=author, recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Этот рецепт уже добавлен в список избранных.',
            })
        return {
            'author': author,
            'recipe': recipe,
        }


class ShoppingCartSerializer(serializers.ModelSerializer):
    recipe = RecipeShortSerializers(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('recipe', )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep['recipe']

    def validate(self, attrs):
        request = self.context['request']
        recipe = get_object_or_404(
            Recipe,
            pk=request.parser_context['kwargs'].get('recipe_id')
        )
        author = request.user

        if ShoppingCart.objects.filter(
                author=author, recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Этот рецепт уже добавлен в список покупок.',
            })
        return {
            'author': author,
            'recipe': recipe,
        }
