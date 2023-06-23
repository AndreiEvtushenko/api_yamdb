from django.core.mail import send_mail


def send_fake_email(username, confirmation_code, email):
    """Делает вид, что отправляет сообщения"""
    send_mail(
        'Confirmation_code',
        f'Username: {username}, confirmation_code: {confirmation_code}',
        'valid@yamdb.fake',
        [f'{email}'],
        fail_silently=False,
    )
