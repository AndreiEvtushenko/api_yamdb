from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверяет корректность года выпуска"""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Год выпуска произведения не может быть больше текущего года.'
            f'Вы уазали: "{value}", сейчас: "{current_year}".'
        )
