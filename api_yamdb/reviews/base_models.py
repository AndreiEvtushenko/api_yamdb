from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CommentsReviewModel(models.Model):
    """Базовая модель для классов Comments и Review"""

    text = models.TextField(
        verbose_name='Отзыв',
        help_text="Введите отзыв, поле обязательное.",
        blank=False
    )

    pub_date = models.DateField(
        verbose_name='Дата',
        auto_now=True
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.text
