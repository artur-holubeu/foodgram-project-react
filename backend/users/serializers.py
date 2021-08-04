from abc import ABC

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import NotFound
from .models import Subscription
from rest_framework import status
from djoser.serializers import UserCreateSerializer
from django.shortcuts import get_object_or_404
from recipes.serializers import RecipesSerializers

User = get_user_model()


class UserBaseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribed')

    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    username = serializers.SlugField(
        allow_unicode=True,
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],

    )

    first_name = serializers.CharField(
        required=True,
        max_length=150
    )

    last_name = serializers.CharField(
        required=True,
        max_length=150,
    )

    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=150,
    )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return False
        return obj.following.filter(user=user).exists()

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep.pop('password', None)
        return rep


class CreateAccountSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class SubscriptionsSerializer(UserBaseSerializer):
    recipes = RecipesSerializers(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes')


class SubscribeSerializer(SubscriptionsSerializer):
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes')

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        recipes_limit = int(
            self.context['request'].query_params.get('recipes_limit')
        )
        rep['recipes'] = rep['recipes'][:recipes_limit]
        return rep

    def validate(self, data):
        author_id = self.context['request'].parser_context['kwargs'].get(
            'author_id')
        if not User.objects.filter(pk=author_id).exists():
            raise NotFound({
                'detail': 'Страница не найдена.',
            }, code=status.HTTP_404_NOT_FOUND)

        current_user = self.context['request'].user
        author = User.objects.get(pk=author_id)
        if author.id == current_user.id:
            raise serializers.ValidationError({
                'errors': ('Пользователь не может быть подписан '
                           'на самого себя.'),
            })

        if Subscription.objects.filter(
                user=current_user, following=author).exists():
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
            'user': current_user,
            'following': author
        }

    def create(self, validated_data):
        return Subscription.objects.create(
            user=validated_data['user'],
            following=validated_data['following']
        ).following


class UnsubscribeSerializer(serializers.Serializer):

    def validate(self, data):
        author_id = self.initial_data.get('author_id')
        if not User.objects.filter(pk=author_id).exists():
            raise NotFound({
                'detail': 'Страница не найдена.',
            }, code=status.HTTP_404_NOT_FOUND)

        current_user = self.initial_data.get('user')
        author = User.objects.get(pk=author_id)
        if not Subscription.objects.filter(
                user=current_user, following=author).exists():
            raise serializers.ValidationError({
                'errors': 'Пользователь еще не подписан на этого автора.',
            })
        return {
            'user': current_user,
            'following': author,
        }

    def save(self, **kwargs):
        user = self.validated_data.get('user')
        following = self.validated_data.get('following')
        Subscription.objects.filter(user=user, following=following).delete()