import random
import string


def create_verification_code():
    """Создает код для подтверждения пользователя"""
    passlength = 6
    a = string.ascii_lowercase
    b = string.ascii_uppercase
    c = string.digits
    d = string.printable
    result = a + b + c + d
    verification_code = ''.join(random.sample(result, passlength))
    return verification_code
