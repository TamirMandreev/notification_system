from django.core.mail import send_mail

from celery import shared_task

from config import settings
from notifications.models import EmailSendStatus, User


@shared_task
def send_async_email(subject, message, user_id, user_email):
    '''
    Асинхронно отправляет эл. сообщение через SMTP-сервер
    :param subject: тема письма
    :param message: текст письма
    :param from_email: email адрес отправителя
    :param recipient_list: список получателей
    :return:
    '''
    try:
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
        )
        if result > 0:
            user = User.objects.get(id=user_id)
            EmailSendStatus.objects.create(user=user, is_successful=True)
        else:
            raise Exception('Сообщение не отправлено')

    except Exception as e:
        user = User.objects.get(id=user_id)
        EmailSendStatus.objects.create(user=user, is_successful=False, error_message=str(e))