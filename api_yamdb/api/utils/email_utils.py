import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('log_bot.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)


# Параметры SMTP-сервера
smtp_server = 'smtp.gmail.com'
smtp_port = 587
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')


def send_code(email: str, confirmation_code: str, username: str) -> None:
    """Отправляет код подтверждения на почту"""
    sender_email = SENDER_EMAIL
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
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
            logging.info('send_code(). Почта успешно отправлена!')
    except Exception as e:
        logging.error(f'send_code(). Возникла ошибка при отправке почты: {e}')
