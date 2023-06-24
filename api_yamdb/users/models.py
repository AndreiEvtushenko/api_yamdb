from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validator import validate_username


ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]

MAX_LENGTH_50 = 50
MAX_LENGTH_150 = 150
MAX_LENGTH_250 = 250
MAX_LENGTH_254 = 254


class User(AbstractUser):
    """Модель пользователей"""

    first_name = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        max_length=MAX_LENGTH_150,
        blank=True
    )

    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        help_text='Введите фамилию пользователя',
        max_length=MAX_LENGTH_150,
        blank=True
    )

    email = models.EmailField(
        blank=False,
        max_length=MAX_LENGTH_254,
        unique=True
    )

    username = models.CharField(
        verbose_name='Уникальное имя пользователя',
        help_text='Введите username',
        blank=False,
        max_length=MAX_LENGTH_150,
        validators=[validate_username,
                    RegexValidator(regex=r'^[\w.@+-]+$',
                                   message=(
                                       'Неправильный формат поля'
                                       'Поле может содержать только буквы,'
                                       'цифры и следующие символы: @ . + -'
                                    ),
                                   code='invalid_field')],
        unique=True
    )

    bio = models.TextField(
        verbose_name='Информация о пользователе',
        help_text='Введите информацию о пользователе',
        blank=True
    )

    role = models.CharField(
        max_length=MAX_LENGTH_50,
        verbose_name='Модель пользователя',
        help_text='Можно выбрать из трех: "user" "moderator" "admin"',
        choices=ROLES,
        default='user',
        blank=True
    )

    confirmation_code = models.CharField(
        max_length=MAX_LENGTH_250,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['username', ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
