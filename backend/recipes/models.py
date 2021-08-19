import re

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name=_('Название тега'),
        help_text=_('Название тега.')
    )
    color = models.CharField(
        unique=True,
        max_length=200,
        verbose_name=_('Цвет тега'),
        help_text=_('Цвет в HEX.')
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name=_('Техническое название тега'),
        help_text=_('Техническое название тега.')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    class Meta:
        verbose_name = _('Ярлык')
        verbose_name_plural = _('Ярлыки')
        ordering = ('-updated_at',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Еесли поле slug заполнено на кириллице - транслитерировать
        в латиницу.
        """
        if bool(re.search('[а-яА-Я]', self.slug)):
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название ингредиента'),
        help_text=_('Название ингредиента.')
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name=_('Система измерений'),
        help_text=_('Система измерений для ингредиента.')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient')
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class IngredientsAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
        verbose_name=_('Ингредиент'),
        help_text=_('Ингредиент необходимый для рецепта.'),
    )
    amount = models.IntegerField(
        verbose_name=_('Количество'),
        help_text=_('Количество ингредиента.'),
        validators=[
            validators.MinValueValidator(
                limit_value=1,
                message='Значение должно быть не меньше 1')]
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления записи'),
        help_text=_('Задается автоматически при обновлении записи.')
    )

    class Meta:
        verbose_name = _('Количество ингредиентов')
        verbose_name_plural = _('Количество ингредиентов')
        ordering = ('ingredient',)

    def __str__(self):
        return f'{self.name} {self.amount} {self.ingredient.measurement_unit}'

    @property
    def name(self):
        return self.ingredient.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        IngredientsAmount,
        related_name='recipes',
        blank=True,
        verbose_name=_('Ингредиенты'),
        help_text=_('Ингредиенты к рецепту.'),
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        verbose_name=_('Теги'),
        help_text=_('Теги рецепта.'),
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название рецепта'),
        help_text=_('Название рецепта.')
    )
    text = models.TextField(
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
        upload_to=_('recipes/images/'),
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

    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')
        ordering = ('-updated_at',)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    author = models.ForeignKey(
        User,
        related_name='shopping_lists',
        on_delete=models.CASCADE,
        verbose_name=_('Автор'),
        help_text=_('Автор листа покупок.'),

    )
    recipe = models.ForeignKey(
        Recipe,
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

    class Meta:
        verbose_name = _('Список покупок')
        verbose_name_plural = _('Списки покупок')
        ordering = ('-updated_at',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'],
                                    name='unique_shopping_list')
        ]

    def __str__(self):
        return self.recipe.name


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

    class Meta:
        verbose_name = _('Список избранных')
        verbose_name_plural = _('Списки избранных')
        ordering = ('-updated_at',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'],
                                    name='unique_favorite_list')
        ]

    def __str__(self):
        return f'{self.author} {self.recipe.name}'
