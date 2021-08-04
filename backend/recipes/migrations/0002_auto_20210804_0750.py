# Generated by Django 3.2.5 on 2021-08-04 07:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Задается автоматически при обновлении записи.', verbose_name='Дата обновления записи')),
            ],
            options={
                'ordering': ('-updated_at',),
            },
        ),
        migrations.CreateModel(
            name='MeasurementUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Полное название системы исчесления.', max_length=200, unique=True, verbose_name='Название системы исчесления')),
                ('short_name', models.CharField(help_text='Короткое название системы исчесления.', max_length=10, unique=True, verbose_name='Название системы исчесления')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Задается автоматически при обновлении записи.', verbose_name='Дата обновления записи')),
            ],
            options={
                'ordering': ('-updated_at',),
            },
        ),
        migrations.AlterModelOptions(
            name='favoritelist',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='measurement_unit',
        ),
        migrations.AddField(
            model_name='favoritelist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Задается автоматически при обновлении записи.', verbose_name='Дата обновления записи'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Задается автоматически при обновлении записи.', verbose_name='Дата обновления записи'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Задается автоматически при обновлении записи.', verbose_name='Дата обновления записи'),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Задается автоматически при обновлении записи.', verbose_name='Дата обновления записи'),
        ),
        migrations.AddField(
            model_name='tag',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Задается автоматически при обновлении записи.', verbose_name='Дата обновления записи'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(help_text='Название ингредиента.', max_length=200, unique=True, verbose_name='Название ингредиента'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(help_text='Время приготовления (в минутах).', validators=[django.core.validators.MinValueValidator(limit_value=1, message='Значение должно быть больше 0')], verbose_name='Время приготовления'),
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Название рецепта.', max_length=200, verbose_name='Название рецепта'),
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='Тэги рецепта.', related_name='recipes', to='recipes.Tag', verbose_name='Тэги'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(help_text='Полное пошаговое описание рецепта.', verbose_name='Описание рецепта'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='Цвет в HEX.', max_length=200, verbose_name='Цвет тэга'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Название тэга.', max_length=200, verbose_name='Название тэга'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(help_text='Техническое название тэга.', max_length=200, verbose_name='Техническое название тэга'),
        ),
        migrations.CreateModel(
            name='RecipeIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(help_text='Количество ингредиента.', validators=[django.core.validators.MinValueValidator(limit_value=0, message='Значение должно быть не меньше 0')], verbose_name='Количество')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Задается автоматически при обновлении записи.', verbose_name='Дата обновления записи')),
                ('ingredient', models.ForeignKey(help_text='Ингреденет необходимый для рецепта.', on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.ingredientunit', verbose_name='Ингредиент')),
                ('recipe', models.ForeignKey(help_text='Рецепт для которого используются ингреденеты.', on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'ordering': ('-updated_at',),
            },
        ),
        migrations.AddConstraint(
            model_name='measurementunit',
            constraint=models.UniqueConstraint(fields=('name', 'short_name'), name='unique_measurement_unit'),
        ),
        migrations.AddField(
            model_name='ingredientunit',
            name='ingredient',
            field=models.ForeignKey(help_text='Ингридиент используемый единцу исчесления.', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_unit', to='recipes.ingredient', verbose_name='Ингридиент'),
        ),
        migrations.AddField(
            model_name='ingredientunit',
            name='measurement_unit',
            field=models.ForeignKey(help_text='Система измерений для ингредиента.', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_unit', to='recipes.measurementunit', verbose_name='Система измерений'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, help_text='Ингридиенты к рецепту.', related_name='recipes', to='recipes.IngredientUnit', verbose_name='Ингридиенты'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт из листа покупок.', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_lists', to='recipes.recipeingredients', verbose_name='Рецепт'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredients',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='ingredientunit',
            constraint=models.UniqueConstraint(fields=('ingredient', 'measurement_unit'), name='unique_ingredient_unit'),
        ),
    ]
