from rest_framework import serializers
from .models import Recipe, Tag


class RecipesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class TagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

