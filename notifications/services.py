import os.path

from django.core.mail import send_mail

import requests
from django.utils import timezone

from smsaero import SmsAero, SmsAeroException

from django.conf import settings
from notifications.models import EmailSendStatus, TelegramSendStatus, SmsSendStatus, Notification

from notifications.models import User


def create_users(users):
    for user in users:
        User.objects.create(name=user[0], email=user[1], number=user[2], tg_chat_id=user[3])


def send_email_message(subject: str, message: str):
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
    failed_email_statuses = EmailSendStatus.objects.filter(is_successful=False)

    for emails_status in failed_email_statuses:
        params = {
            'text': full_message,
            'chat_id': emails_status.user.tg_chat_id,
        }
        response = requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)
        if response.status_code == 200:
            TelegramSendStatus.objects.create(user=emails_status.user, is_successful=True)
        else:
            TelegramSendStatus.objects.create(user=emails_status.user, is_successful=False, error_message=response.status_code)


def send_sms_message(message: str) -> dict:
    '''
    Отправляет смс-сообщения

    Параметры:
    phone (int): Номер телефона в формате +79915410704, на который будет отправлено смс-сообщение
    message (str): Содержание отправляемого смс-сообщения

    Возвращает:
    dict: Словарь, содержащий ответ от API SmsAero
    '''
    api = SmsAero(settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)
    telegram_send_status_false = TelegramSendStatus.objects.filter(is_successful=False)
    for telegram_status in telegram_send_status_false:
        try:
            phone = int(telegram_status.user.number)
            api.send_sms(phone, message)
            SmsSendStatus.objects.create(user=telegram_status.user, is_successful=True)
        except SmsAeroException as e:
            SmsSendStatus.objects.create(user=telegram_status.user, is_successful=False, error_message=e)


def generate_notification_report(output_file=False):
    '''
    Генерирует текстовый отчет по всем отправкам
    :return:
    '''

    timestamp = timezone.now().strftime('%d.%m.%Y %H:%M')
    file_name = f'{timestamp}.txt'
    file_path = os.path.join(settings.MEDIA_ROOT, 'reports', file_name)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('ОТЧЕТ ПО ОТПРАВКЕ УВЕДОМЛЕНИЙ\n')
        f.write('=' * 50 + '\n\n')

        # Статистика по Email
        email_total = EmailSendStatus.objects.count()
        email_success = EmailSendStatus.objects.filter(is_successful=True).count()
        email_failed = email_total - email_success

        f.write('ЭЛЕКТРОННАЯ ПОЧТА:\n')
        f.write(f'\tВсего отправок: {email_total}\n')
        f.write(f'\tУспешных: {email_success}\n')
        f.write(f'\tНеудачных: {email_failed}\n')

        # Статистика по Telegram
        tg_total = TelegramSendStatus.objects.count()
        tg_success = TelegramSendStatus.objects.filter(is_successful=True).count()
        tg_failed = tg_total - tg_success

        f.write('TELEGRAM:\n')
        f.write(f'\tВсего отправок: {tg_total}\n')
        f.write(f'\tУспешных: {tg_success}\n')
        f.write(f'\tНеудачных: {tg_failed}\n')

        # Статистика по SMS
        sms_total = SmsSendStatus.objects.count()
        sms_success = SmsSendStatus.objects.filter(is_successful=True).count()
        sms_failed = sms_total - sms_success

        f.write('SMS:\n')
        f.write(f'\tВсего отправок: {sms_total}\n')
        f.write(f'\tУспешных: {sms_success}\n')
        f.write(f'\tНеудачных: {sms_failed}\n')

        # Детали по неудачным отправкам
        f.write('\nНЕУДАЧНЫЕ ОТПРАВКИ:\n')
        f.write('-' * 30 + '\n')

        failed_emails = EmailSendStatus.objects.filter(is_successful=False)
        if failed_emails.exists():
            f.write('Email:\n')
            for attempt in failed_emails:
                f.write(f'\tПользователь: {attempt.user.email}\n')
                f.write(f'\tВремя: {attempt.sent_attempted}\n')
                f.write(f'\tОшибка: {attempt.error_message}\n')
                f.write(f'\t---\n')

        failed_tg = TelegramSendStatus.objects.filter(is_successful=False)
        if failed_tg.exists():
            f.write('Telegram:\n')
            for attempt in failed_tg:
                f.write(f'\tПользователь: {attempt.user.email}\n')
                f.write(f'\tВремя: {attempt.sent_attempted}\n')
                f.write(f'\tОшибка: {attempt.error_message}\n')
                f.write('\t---\n')

        failed_sms = SmsSendStatus.objects.filter(is_successful=False)
        if failed_sms.exists():
            f.write('Sms:\n')
            for attempt in failed_sms:
                f.write(f'\tПользователь: {attempt.user.email}\n')
                f.write(f'\tВремя: {attempt.sent_attempted}\n')
                f.write(f'\tОшибка: {attempt.error_message}\n')
                f.write('\t---\n')


def delete_objects():
    '''
    Удаляет все объекты моделей User, Notification, EmailSendStatus, TelegramSendStatus, SmsSendStatus
    '''
    User.objects.all().delete()
    Notification.objects.all().delete()
    EmailSendStatus.objects.all().delete()
    TelegramSendStatus.objects.all().delete()
    SmsSendStatus.objects.all().delete()