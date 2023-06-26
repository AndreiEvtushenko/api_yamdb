from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from .base_models import CommentsReviewModel
from .validators import validate_year

User = get_user_model()

MAX_LENGTH_50: int = 50
MAX_LENGTH_256: int = 256


class Categories(models.Model):
    """Модель категорий"""

    name = models.CharField(
        verbose_name='Название категории',
        help_text='Введите название категории, это поле обязательное',
        max_length=MAX_LENGTH_256,
        blank=False
    )

    slug = models.SlugField(
        verbose_name='Слаг категории',
        help_text='Это обязательное поле с уникальным значением',
        max_length=MAX_LENGTH_50,
        blank=False,
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genres(models.Model):
    """Модель жанров"""

    name = models.CharField(
        verbose_name='Название жанра',
        help_text='Введите название жанра, это поле обязательное',
        max_length=MAX_LENGTH_256,
        blank=False
    )

    slug = models.SlugField(
        verbose_name='Слаг жанра',
        help_text='Введите слаг жанра, слаг должен быть уникальным',
        max_length=MAX_LENGTH_50,
        blank=False,
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений"""

    name = models.CharField(
        verbose_name='Название произведения',
        help_text='Введите название произведения, это поле обязательное',
        max_length=MAX_LENGTH_256,
        blank=False,
        unique=True,
        db_index=True
    )

    year = models.IntegerField(
        verbose_name='Год выхода',
        validators=[validate_year],
        blank=False,
        db_index=True
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

    def __str__(self) -> str:
        return self.name


class Review(CommentsReviewModel):
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

    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        help_text='Рейтинг от 1 до 10',
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(10)],
        blank=False,
        db_index=True
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


class Comments(CommentsReviewModel):
    """Модель комментариев"""

    author = models.ForeignKey(
        User,
        related_name='comments_authors',
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=False
    )

    reviews_id = models.ForeignKey(
        Review,
        related_name='comment_Reviews',
        help_text='id отзыва, обязательное поле.',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class GenreTitle(models.Model):
    """Модель связи Title с Genres"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_index=True
    )

    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр фильма'
        verbose_name_plural = 'Жанры фильма'

    def __str__(self) -> str:
        return f'{self.title} {self.genre}'
