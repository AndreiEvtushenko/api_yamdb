import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Параметры SMTP-сервера
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = ''
smtp_password = 'awlmubbnmxbjsapt'


def send_code(email, confirmation_code, username):
    """Отправляет код подтверждения на почту"""
    sender_email = 'evtushenkoad@gmail.com'
    receiver_email = email

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'verification_code'

    message_text = (f'Привет, {username}.'
                    f'Проверочный код: {confirmation_code}.')
    message.attach(MIMEText(message_text, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
            print('Почта успешно отправлена!')
    except Exception as e:
        print('Возникла ошибка при отправке почты:', str(e))
