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
        blank=False
    )
    confirmation_code = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
