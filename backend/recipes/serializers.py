from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import Subscription
from users.serializers import UserBaseSerializer

from .models import (
    FavoriteList, Ingredient, IngredientsAmount, Recipe, ShoppingCart, Tag,
)

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
    amount = serializers.IntegerField(
        write_only=True,
        min_value=1,
        max_value=99999
    )

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'amount')


class RecipeSerializers(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    author = UserBaseSerializer(read_only=True)
    ingredients = IngredientAmountSerializers(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['tags'] = TagSerializers(instance.tags.all(), many=True).data

        rep['ingredients'] = [{
            **IngredientSerializers(x.ingredient).data,
            **{'amount': x.amount}
        } for x in instance.ingredients.all().select_related('ingredient')]
        return rep

    def validate_ingredients(self, attrs) -> list:
        if self.context['request'].method != 'PATCH' and not attrs:
            raise serializers.ValidationError(
                'At least one ingredient must be added.'
            )
        ingredients = {}
        for item in attrs:
            if ingredients.get(item.get('id')):
                ingredients[item.get('id')] += item.get('amount')
            else:
                ingredients[item.get('id')] = item.get('amount')

        return [
            {'ingredient': ingredient, 'amount': amount}
            for ingredient, amount in ingredients.items()
        ]

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        ingredients = [IngredientsAmount.objects.create(**x) for x in
                       ingredients]
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

    def get_is_favorited(self, instance):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return instance.favorite_lists.filter(author=user).exists()

    def get_is_in_shopping_cart(self, instance):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return instance.shopping_lists.filter(author=user).exists()

    def _update_ingredients(self):
        new_data_raw = self.validated_data.get('ingredients')
        if new_data_raw:
            self.instance.ingredients.all().delete()
            ingredients = [
                IngredientsAmount.objects.create(**x) for x in new_data_raw
            ]
            self.instance.ingredients.add(*ingredients)

    def _update_tags(self):
        new_data_raw = self.validated_data.get('tags')
        if new_data_raw:
            self.instance.tags.clear()
            self.instance.tags.add(*self.validated_data['tags'])


class RecipeShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscriptionsSerializer(UserBaseSerializer):
    recipes = RecipeShortSerializers(many=True, read_only=True)

    class Meta(UserBaseSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',
                            'is_subscribed')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['recipes_count'] = len(rep['recipes'])
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit')
        if recipes_limit:
            rep['recipes'] = rep['recipes'][:int(recipes_limit)]
        return rep


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'following',)
        read_only_fields = ('user', 'following',)

    def to_representation(self, instance):
        return SubscriptionsSerializer(
            instance.following,
            context={'request': self.context.get('request')}
        ).data

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


class FavoriteListSerializer(serializers.ModelSerializer):
    recipe = RecipeShortSerializers(read_only=True)

    class Meta:
        model = FavoriteList
        fields = ('recipe',)

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
        fields = ('recipe',)

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
