from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from .validator import validate_username


ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        max_length=150,
        blank=True)
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        help_text='Введите фамилию пользователя',
        max_length=150,
        blank=True)
    email = models.EmailField(
        blank=False,
        max_length=254,
        unique=True
        )
    username = models.CharField(
        verbose_name='Уникальное имя пользователя',
        help_text='Введите username',
        blank=False,
        max_length=150,
        validators=[validate_username,
                    RegexValidator(regex=r'^[\w.@+-]+$',
                                   message='Неправильный формат поля',
                                   code='invalid_field')],
        unique=True
        )
    bio = models.TextField(
        verbose_name='Информация о пользователе',
        help_text='Введите информацию о пользователе',
        blank=True
    )
    role = models.CharField(
        max_length=50,
        verbose_name='Модель пользователя',
        help_text='Можно выбрать из трех: "user" "moderator" "admin"',
        choices=ROLES,
        default='user',
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=250,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
