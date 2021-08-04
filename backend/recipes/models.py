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
        verbose_name=_('Название тэга'),
        help_text=_('Название тэга.')
    )
    color = models.CharField(
        max_length=200,
        verbose_name=_('Цвет тэга'),
        help_text=_('Цвет в HEX.')
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('Техническое название тэга'),
        help_text=_('Техническое название тэга.')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
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

    class Meta:
        ordering = ('-updated_at',)


class MeasurementUnit(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=200,
        verbose_name=_('Название системы исчесления'),
        help_text=_('Полное название системы исчесления.')
    )
    short_name = models.CharField(
        blank=False,
        unique=True,
        max_length=10,
        verbose_name=_('Название системы исчесления'),
        help_text=_('Короткое название системы исчесления.')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    def __str__(self):
        return f'{self.name} ({self.short_name})'

    class Meta:
        ordering = ('-updated_at',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'short_name'],
                                    name='unique_measurement_unit')
        ]


class Ingredient(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=200,
        verbose_name=_('Название ингредиента'),
        help_text=_('Название ингредиента.')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-updated_at',)


class IngredientUnit(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredients_unit',
        on_delete=models.CASCADE,
        verbose_name=_('Ингридиент'),
        help_text=_('Ингридиент используемый единцу исчесления.'),
    )
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        related_name='ingredients_unit',
        on_delete=models.CASCADE,
        verbose_name=_('Система измерений'),
        help_text=_('Система измерений для ингредиента.')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    def __str__(self):
        return f'{self.ingredient.name} ({self.measurement_unit.short_name})'

    class Meta:
        ordering = ('-updated_at',)
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'measurement_unit'],
                                    name='unique_ingredient_unit')
        ]


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        IngredientUnit,
        related_name='recipes',
        blank=True,
        verbose_name=_('Ингридиенты'),
        help_text=_('Ингридиенты к рецепту.'),
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        verbose_name=_('Тэги'),
        help_text=_('Тэги рецепта.'),
    )
    name = models.CharField(
        blank=False,
        max_length=200,
        verbose_name=_('Название рецепта'),
        help_text=_('Название рецепта.')
    )
    text = models.TextField(
        blank=False,
        verbose_name=_('Описание рецепта'),
        help_text=_('Полное пошаговое описание рецепта.')
    )
    cooking_time = models.IntegerField(
        verbose_name=_('Время приготовления'),
        help_text=_('Время приготовления (в минутах).'),
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
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name=_('Автор'),
        help_text=_('Автор рецепта.'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-updated_at',)


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
        verbose_name=_('Рецепт'),
        help_text=_('Рецепт для которого используются ингреденеты.'),
    )
    ingredient = models.ForeignKey(
        IngredientUnit,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
        verbose_name=_('Ингредиент'),
        help_text=_('Ингреденет необходимый для рецепта.'),
    )
    amount = models.FloatField(
        verbose_name=_('Количество'),
        help_text=_('Количество ингредиента.'),
        validators=[
            validators.MinValueValidator(
                limit_value=0,
                message='Значение должно быть не меньше 0')]
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    def __str__(self):
        return f'{self.recipe.name} {self.ingredient.ingredient.name}'

    class Meta:
        ordering = ('-updated_at',)
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_recipe_ingredient')
        ]


class ShoppingList(models.Model):
    author = models.ForeignKey(
        User,
        related_name='shopping_lists',
        on_delete=models.CASCADE,
        verbose_name=_('Автор'),
        help_text=_('Автор листа покупок.'),

    )
    recipe = models.ForeignKey(
        RecipeIngredients,
        related_name='shopping_lists',
        on_delete=models.CASCADE,
        verbose_name=_('Рецепт'),
        help_text=_('Рецепт из листа покупок.'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    def __str__(self):
        return self.recipe

    class Meta:
        ordering = ('-updated_at',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'],
                                    name='unique_shopping_list')
        ]


class FavoriteList(models.Model):
    author = models.ForeignKey(
        User,
        related_name='favorite_lists',
        on_delete=models.CASCADE,
        verbose_name=_('Автор'),
        help_text=_('Автор листа избранного.'),

    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite_lists',
        on_delete=models.CASCADE,
        verbose_name=_('Рецепт'),
        help_text=_('Рецепт из листа избранного.'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    def __str__(self):
        return f'{self.author} {self.recipe}'

    class Meta:
        ordering = ('-updated_at',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'],
                                    name='unique_favorite_list')
        ]
