from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from users.models import Subscription
from users.serializers import UserBaseSerializer

from .models import (FavoriteList, Ingredient, IngredientsAmount, Recipe,
                     ShoppingCart, Tag)

User = get_user_model()


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmount(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, instant):
        return instant.ingredient.name

    def get_id(self, instant):
        return instant.ingredient.id

    def get_measurement_unit(self, instant):
        return instant.ingredient.measurement_unit


class RecipeSerializers(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserBaseSerializer(read_only=True)
    tags = TagSerializers(many=True, read_only=True)
    ingredients = IngredientAmount(many=True, read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def to_internal_value(self, data):
        self._to_internal_value_ingredients()
        self._to_internal_value_tags()
        self._to_internal_value_image()
        data['author'] = self.context['request'].user
        return data

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        ingredients_serializer = self.fields['ingredients']
        ingredients_for_recipes = ingredients_serializer.create(ingredients)
        recipe.tags.add(*tags)
        recipe.ingredients.add(*ingredients_for_recipes)
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

    def get_is_favorited(self, instant):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return False
        return FavoriteList.objects.filter(author=user,
                                           recipe=instant).exists()

    def get_is_in_shopping_cart(self, instant):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return False
        return ShoppingCart.objects.filter(author=user,
                                           recipe=instant).exists()

    def _to_internal_value_image(self):
        image = self.initial_data.get('image')
        self.initial_data['image'] = Base64ImageField().to_internal_value(
            image)

    def _to_internal_value_ingredients(self):
        ingredients = self.initial_data.get('ingredients')
        if self.context['request'].method != 'PATCH' and not ingredients:
            raise serializers.ValidationError(
                'Должен быть добавлен хотя бы один ингредиент.'
            )

        if ingredients:
            ingredients_id = [x.get('id') for x in ingredients]
            ingredients_obj = Ingredient.objects.filter(pk__in=ingredients_id)
            if err_id := set(ingredients_id) ^ set(
                    x.id for x in ingredients_obj):
                raise serializers.ValidationError(
                    {
                        'errors': 'Переданы несуществующие ингредиенты',
                        'id': list(err_id),
                    }
                )
            try:
                self.initial_data['ingredients'] = [
                    {
                        'ingredient': ingredients_obj.get(pk=x.get('id')),
                        'amount': int(x.get('amount')),
                    }
                    for x in ingredients]
            except ValueError:
                raise serializers.ValidationError(
                    {
                        'errors': 'Значение для количества ингредиента должен '
                                  'быть числом.',
                    },
                )
        else:
            self.initial_data['ingredients'] = []

    def _to_internal_value_tags(self):
        tags = self.initial_data.get('tags')
        if self.context['request'].method != 'PATCH' and not tags:
            raise serializers.ValidationError(
                'Должен быть добавлен хотя бы один tag.')
        if tags:
            tags_obj = Tag.objects.filter(pk__in=tags)
            if err_id := set(tags) ^ set(x.id for x in tags_obj):
                raise serializers.ValidationError({
                    'errors': 'Переданы несуществующие tag',
                    'id': list(err_id),
                })
            self.initial_data['tags'] = tags_obj
        else:
            self.initial_data['tags'] = []

    def _update_ingredients(self, name_param='ingredients'):
        new_data_raw = self.validated_data[name_param]
        if new_data_raw:
            self.instance.ingredients.all().delete()
            new_data_serializer = self.fields[name_param]
            new_data_serialized = new_data_serializer.create(new_data_raw)
            self.instance.ingredients.add(*new_data_serialized)

    def _update_tags(self, name_param='tags'):
        new_data_raw = self.validated_data[name_param]
        if new_data_raw:
            self.instance.tags.clear()
            self.instance.tags.add(*self.validated_data[name_param])


class RecipeShortSerializers(RecipeSerializers):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionsSerializer(UserBaseSerializer):
    recipes = RecipeShortSerializers(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes'
        )
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        recipes_limit = int(
            self.context['request'].query_params.get('recipes_limit')
        )
        rep['recipes_count'] = len(rep['recipes'])
        rep['recipes'] = rep['recipes'][:recipes_limit]
        return rep

    def validate(self, data):
        following_id = self.context['request'].parser_context['kwargs'].get(
            'following_id')

        if not User.objects.filter(pk=following_id).exists():
            raise NotFound({
                'detail': 'Страница не найдена.',
            }, code=status.HTTP_404_NOT_FOUND)

        user = self.context['request'].user
        following = User.objects.get(pk=following_id)

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

        recipes_limit = int(
            self.context['request'].query_params.get('recipes_limit')
        )

        if recipes_limit < 0:
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
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def to_internal_value(self, data):
        recipe_id = self.context['request'].parser_context['kwargs'].get(
            'recipe_id')
        if not Recipe.objects.filter(pk=recipe_id).exists():
            raise NotFound({
                'detail': 'Страница не найдена.',
            }, code=status.HTTP_404_NOT_FOUND)

        author = self.context['request'].user
        recipe = Recipe.objects.get(pk=recipe_id)

        if FavoriteList.objects.filter(
                author=author, recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Этот рецепт уже добавлен в список избранных.',
            })
        return {
            'author': author,
            'recipe': recipe
        }

    def create(self, validated_data):
        return FavoriteList.objects.create(
            author=validated_data['author'],
            recipe=validated_data['recipe'],
        ).recipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def to_internal_value(self, data):
        recipe_id = self.context['request'].parser_context['kwargs'].get(
            'recipe_id')
        if not Recipe.objects.filter(pk=recipe_id).exists():
            raise NotFound({'detail': 'Страница не найдена.'})

        author = self.context['request'].user
        recipe = Recipe.objects.get(pk=recipe_id)

        if ShoppingCart.objects.filter(
                author=author, recipe=recipe).exists():
            raise serializers.ValidationError({
                'errors': 'Этот рецепт уже добавлен в список покупок.',
            })
        return {
            'author': author,
            'recipe': recipe
        }

    def create(self, validated_data):
        return ShoppingCart.objects.create(
            author=validated_data['author'],
            recipe=validated_data['recipe'],
        ).recipe
