from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserBaseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribed')

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

    def validate(self, attr):
        super().validate(attr)
        if len(attr.get('password')) >= 150:
            raise ValidationError({
                'password': ('Ensure this field has no more '
                             'than 150 characters.')
            })
        return attr
