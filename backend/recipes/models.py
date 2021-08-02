from slugify import slugify
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import re


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        blank=False,
        max_length=200,
        verbose_name=_('Название тэга.'),
        help_text=_('Название тэга.')
    )
    color = models.CharField(
        max_length=200,
        verbose_name=_('Цвет тэга.'),
        help_text=_('Цвет в HEX.')
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('Техническое название тэга'),
        help_text=_('Техническое название тэга')
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Еесли поле slug заполнено на кириллице - транслитерировать
        в латиницу.
        """
        if bool(re.search('[а-яА-Я]', self.slug)):
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)


class MeasurementUnit(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=200,
        verbose_name=_('Название системы исчесления.'),
        help_text=_('Полное название системы исчесления.')
    )
    short_name = models.CharField(
        blank=False,
        unique=True,
        max_length=10,
        verbose_name=_('Название системы исчесления.'),
        help_text=_('Короткое название системы исчесления.')
    )

    def __str__(self):
        return self.short_name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'short_name'],
                                    name='unique_measurement_unit')
        ]


class Ingredient(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=200,
        verbose_name=_('Название ингредиента.'),
        help_text=_('Название ингредиента.')
    )

    def __str__(self):
        return {self.name}


class IngredientUnit(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name="ingredients_unit",
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
        help_text="Ингридиент используемый единцу исчесления.",
    )
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        related_name="ingredients_unit",
        on_delete=models.CASCADE,
        verbose_name=_('Система измерений'),
        help_text=_('Система измерений для ингредиента')
    )

    def __str__(self):
        return f'{self.ingredient} ({self.measurement_unit})'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ingredient", "measurement_unit"],
                                    name="unique_ingredient_unit")
        ]


class Recipe(models.Model):
    ingredients = models.ForeignKey(
        IngredientUnit,
        related_name="recipes",
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
        help_text="Ингридиенты к рецепту",
    )
    tags = models.ForeignKey(
        Tag,
        related_name="recipes",
        on_delete=models.CASCADE,
        verbose_name="Тэги",
        help_text="Тэги рецепта",
    )
    name = models.CharField(
        blank=False,
        max_length=200,
        verbose_name=_('Название рецепта.'),
        help_text=_('Название рецепта.')
    )
    text = models.TextField(
        blank=False,
        verbose_name=_('Описание рецепта.'),
        help_text=_('Описание рецепта.')
    )
    cooking_time = models.IntegerField(
        verbose_name=_('Время приготовления'),
        help_text=_('Время приготовления (в минутах)'),
        validators=[
            validators.MinValueValidator(
                limit_value=1,
                message='Значение должно быть больше 0')]
    )
    image = models.ImageField(
        upload_to='media',
        verbose_name=_('Картинка рецепта'),
        help_text=_('Картинка рецепта.'),
    )
    author = models.ForeignKey(
        User,
        related_name="recipes",
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Автор рецепта.",
    )

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_ingredients",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        help_text="Рецепт для которого используются ингреденеты.",
    )
    ingredient = models.ForeignKey(
        IngredientUnit,
        related_name="recipe_ingredients",
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        help_text="Ингреденет необходимый для рецепта.",
    )
    amount = models.IntegerField(
        verbose_name=_('Количество'),
        help_text=_('Количество ингредиента'),
        validators=[
            validators.MinValueValidator(
                limit_value=0,
                message='Значение должно быть не меньше 0')]
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["recipe", "ingredient"],
                                    name="unique_recipe_ingredient")
        ]


class ShoppingList(models.Model):
    author = models.ForeignKey(
        User,
        related_name="shopping_lists",
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Автор листа покупок.",

    )
    recipe = models.ForeignKey(
        RecipeIngredients,
        related_name="shopping_lists",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        help_text="Рецепт из листа покупок.",
    )

    def __str__(self):
        return self.recipe

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["author", "recipe"],
                                    name="unique_shopping_list")
        ]


class FavoriteList(models.Model):
    author = models.ForeignKey(
        User,
        related_name="favorite_lists",
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Автор листа избранного.",

    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="favorite_lists",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        help_text="Рецепт из листа избранного.",
    )

    def __str__(self):
        return self.recipe

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["author", "recipe"],
                                    name="unique_favorite_list")
        ]
