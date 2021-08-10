# Generated by Django 3.2.5 on 2021-08-10 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='author',
            field=models.ForeignKey(help_text='Автор листа покупок.', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_lists', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт из листа покупок.', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_lists', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(help_text='Автор рецепта.', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, help_text='Ингридиенты к рецепту.', related_name='recipes', to='recipes.IngredientsAmount', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='Тэги рецепта.', related_name='recipes', to='recipes.Tag', verbose_name='Тэги'),
        ),
        migrations.AddField(
            model_name='ingredientsamount',
            name='ingredient',
            field=models.ForeignKey(help_text='Ингреденет необходимый для рецепта.', on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient'),
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='author',
            field=models.ForeignKey(help_text='Автор листа избранного.', on_delete=django.db.models.deletion.CASCADE, related_name='favorite_lists', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт из листа избранного.', on_delete=django.db.models.deletion.CASCADE, related_name='favorite_lists', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('author', 'recipe'), name='unique_shopping_list'),
        ),
        migrations.AddConstraint(
            model_name='favoritelist',
            constraint=models.UniqueConstraint(fields=('author', 'recipe'), name='unique_favorite_list'),
        ),
    ]
