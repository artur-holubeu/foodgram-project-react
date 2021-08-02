from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserCreateSerializer, UserSerializer



User = get_user_model()


class AuthCreateAccountSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')

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

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        rep.pop('password', None)
        return rep


class AuthUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
