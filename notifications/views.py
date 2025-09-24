from rest_framework.generics import CreateAPIView
from django.conf import settings
from celery import chain

from notifications.serializers import NotificationSerializer
from notifications.services import create_users
from notifications.models import User

from notifications.tasks import send_async_email, send_telegram_message


class NotificationCreateAPIView(CreateAPIView):
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        serializer.save()

        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']

        # Создать пользователей
        create_users(serializer.validated_data['users'])

        # Отправить каждому пользователю письмо на эл. почту
        send_async_email.delay(subject, message)
        # Кому не получилось отправить на эл. почту, отправить в Telegram
        send_telegram_message.delay(subject, message)
        # Отправить пользователям смс




