from django.core.mail import send_mail

from celery import shared_task

from config import settings
from notifications.models import EmailSendStatus, User


@shared_task
def send_async_email(subject, message):
    '''
    Асинхронно отправляет эл. сообщение через SMTP-сервер всем пользователям
    :param subject: тема письма
    :param message: текст письма
    :return:
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