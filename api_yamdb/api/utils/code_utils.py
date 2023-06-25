import random
import string


def create_verification_code() -> str:
    """Создает код для подтверждения пользователя"""
    passlength = 6
    characters = (string.ascii_lowercase +
                  string.ascii_uppercase +
                  string.digits +
                  string.printable)
    return ''.join(random.sample(characters, passlength))
