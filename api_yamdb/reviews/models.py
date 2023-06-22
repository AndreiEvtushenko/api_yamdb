from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models

from .validators import validate_year

User = get_user_model()


class Categories(models.Model):
    """Модель категорий"""
    name = models.CharField(
        verbose_name='Название категории',
        help_text='Введите название категории, это поле обязательное',
        max_length=256,
        blank=False,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        help_text='Это обязательное поле с уникальным значением',
        max_length=50,
        blank=False,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genres(models.Model):
    """Модель жанров"""
    name = models.CharField(
        verbose_name='Название жанра',
        help_text='Введите название жанра, это поле обязательное',
        max_length=256,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        help_text='Введите слаг жанра, слаг должен быть уникальным',
        max_length=50,
        blank=False,
        # unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведений"""
    name = models.CharField(
        verbose_name='Название произведения',
        help_text='Введите название произведения, это поле обязательное',
        max_length=256,
        blank=False,
        unique=True
    )
    year = models.IntegerField(
        verbose_name='Год выхода',
        validators=[validate_year],
        blank=False
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        help_text='Введите описания произведения'
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitle',
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
        help_text='Введите категорию произведения, поле обязательное'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов"""
    author = models.ForeignKey(
        User,
        related_name='reviews_authors',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=False
    )
    title = models.ForeignKey(
        Title,
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    """Модель комментариев"""
    author = models.ForeignKey(
        User,
        related_name='comments_author',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=False
    )
    reviews_id = models.ForeignKey(
        Review,
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

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class GenreTitle(models.Model):
    """Модель жанров"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title} {self.genre}'
