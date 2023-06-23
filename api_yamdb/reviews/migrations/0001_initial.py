# Generated by Django 3.2 on 2023-06-22 17:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории, это поле обязательное', max_length=256, unique=True, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Это обязательное поле с уникальным значением', unique=True, verbose_name='Слаг категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст комментария, обязательное поле.', verbose_name='Текст комментария')),
                ('pub_date', models.DateField(auto_now=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название жанра, это поле обязательное', max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(help_text='Введите слаг жанра, слаг должен быть уникальным', verbose_name='Слаг жанра')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите отзыв, поле обязательное.', null=True, verbose_name='Отзыв')),
                ('score', models.IntegerField(help_text='Рейтинг от 1 до 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Рейтинг')),
                ('pub_date', models.DateField(auto_now=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название произведения, это поле обязательное', max_length=256, unique=True, verbose_name='Название произведения')),
                ('year', models.IntegerField(validators=[reviews.validators.validate_year], verbose_name='Год выхода')),
                ('description', models.TextField(help_text='Введите описания произведения', verbose_name='Описание произведения')),
                ('category', models.ForeignKey(help_text='Введите категорию произведения, поле обязательное', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='reviews.categories', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Введите жанр произведения, поле обязательное', related_name='genres', through='reviews.GenreTitle', to='reviews.Genres', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
    ]
