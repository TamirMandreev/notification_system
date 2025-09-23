from django.core.mail import send_mail

from celery import shared_task

@shared_task
def send_async_email(subject, message, recipient_list):
    return send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_list,
    )