from django.contrib.auth import get_user_model

from .code_utils import create_verification_code
from .fake_email_utils import send_fake_email

User = get_user_model()


def create_send_code(user, username, email):
    """Генерирует код, отправляет код пользователю"""
    confirmation_code = create_verification_code()
    user.confirmation_code = confirmation_code
    user.save()
    send_fake_email(username, confirmation_code, email)
