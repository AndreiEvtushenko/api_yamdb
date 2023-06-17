from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
