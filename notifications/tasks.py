from django.core.mail import send_mail

from celery import shared_task

@shared_task
def send_async_email(subject, message, from_email, recipient_list):
    '''
    Асинхронно отправляет эл. сообщение через SMTP-сервер
    :param subject: тема письма
    :param message: текст письма
    :param from_email: email адрес отправителя
    :param recipient_list: список получателей
    :return:
    '''
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )
        return f'Email успешно отправлен на {recipient_list}'
    except Exception as e:
        return f'Ошибка отправки email: {str(e)}'