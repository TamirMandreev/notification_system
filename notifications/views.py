from rest_framework.generics import CreateAPIView
from django.conf import settings

from notifications.serializers import NotificationSerializer
from notifications.services import create_users, send_users_email
from notifications.models import User

from notifications.tasks import send_async_email


class NotificationCreateAPIView(CreateAPIView):
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        serializer.save()

        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']

        # Создать пользователей
        create_users(serializer.validated_data['users'])
        # Отправить каждому пользователю письмо
        send_async_email.delay(subject, message)
        # Отправить пользователям смс




