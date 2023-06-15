from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

import datetime

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        help_text='Введите название категории, это поле обязательное',
        max_length=256,
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        help_text='Это обязательное поле с уникальным значением',
        max_length=50,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        help_text='Введите название жанра, это поле обязательное',
        max_length=256,
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        help_text='Введите слаг жанра, слаг должен быть уникальным',
        max_length=50,
        blank=False,
        unique=True
    )
    titles = models.ManyToManyField(
        'Titles',
        related_name='genres_titles',
        verbose_name='Фильмы',
        help_text='Выберите фильмы для жанра'
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        help_text='Введите название произведения, это поле обязательное',
        max_length=256,
        blank=False
    )
    year = models.IntegerField(
        verbose_name='Год выхода',
        blank=False
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        help_text='Введите описания произведения'
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='genres',
        verbose_name='Жанр',
        help_text='Введите жанр произведения, поле обязательное',
        blank=False
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Категория',
        help_text='Введите категорию произведения, поле обязательное',
        blank=False
    ) 

    def __str__(self):
        return self.name

    def clean(self):
        """Проверяет корректность года выпуска"""
        current_datetime = datetime.datetime.now()
        current_year = current_datetime.year
        if self.year > current_year:
            raise ValidationError(
                'Год выпуска произведения не может быть больше текущего'
            )


class Reviews(models.Model):
    author = models.ForeignKey(
        User,
        related_name='reviews_authors',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=False
    )
    title_id = models.ForeignKey(
        Titles,
        related_name='reviews_title_id',
        help_text='id произведения, обязательное поле',
        on_delete=models.CASCADE,
        blank=False
    )
    text = models.TextField(
        verbose_name='Отзыв',
        help_text="Введите отзыв, поле обязательное.",
        blank=False,
        null=True
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        help_text='Рейтинг от 1 до 10',
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(10)],
        blank=False
    )
    pub_date = models.DateField(
        verbose_name='Дата',
        auto_now=True
    )


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        related_name='comments_author',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=False
    )
    title_id = models.ForeignKey(
        Reviews,
        related_name='comments_titles_id',
        help_text='id отзыва, обязательное поле.',
        on_delete=models.CASCADE,
        blank=False
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария, обязательное поле.',
        blank=False
    )
    pub_date = models.DateField(
        verbose_name='Дата',
        auto_now=True
    )
