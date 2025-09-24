from django.core.mail import send_mail

import requests

from celery import shared_task
from smsaero import SmsAero, SmsAeroException

from config import settings
from notifications.models import EmailSendStatus, User, TelegramSendStatus



def send_async_email(subject: str, message: str):
    '''
    Отправляет всем пользователям сообщение по эл. почте через SMTP-сервер

    Параметры:
    subject (str): Тема письма
    message (str): Текст письма
    '''
    users = User.objects.all()
    for user in users:
        try:
            result = send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            if result > 0:
                EmailSendStatus.objects.create(user=user, is_successful=True)
            else:
                raise Exception('Сообщение не отправлено')

        except Exception as e:
            EmailSendStatus.objects.create(user=user, is_successful=False, error_message=str(e))



def send_telegram_message(subject: str, message: str):
    '''
    Отправляет сообщение в Telegram

    Параметры:
    subject (str): Тема письма
    message (str): Текст письма
    '''

    full_message = f'Тема: {subject} \n\nСообщение: {message}'
    emails_send_status_false = EmailSendStatus.objects.filter(is_successful=False)

    for emails_status in emails_send_status_false:
        params = {
            'text': full_message,
            'chat_id': emails_status.user.tg_chat_id,
        }
        response = requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)
        if response.status_code == 200:
            TelegramSendStatus.objects.create(user=emails_status.user, is_successful=True)
        else:
            TelegramSendStatus.objects.create(user=emails_status.user, is_successful=False)








@shared_task
def send_sms(phone: int, message: str) -> dict:
    '''
    Отправляет смс-сообщения

    Параметры:
    phone (int): Номер телефона в формате +79915410704, на который будет отправлено смс-сообщение
    message (str): Содержание отправляемого смс-сообщения

    Возвращает:
    dict: Словарь, содержащий ответ от API SmsAero
    '''

    api = SmsAero(settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)
    return api.send_sms(phone, message)
