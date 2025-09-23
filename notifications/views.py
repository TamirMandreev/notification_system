from rest_framework.generics import CreateAPIView
from django.conf import settings

from notifications.serializers import NotificationSerializer
from notifications.services import get_recipient_list

from notifications.tasks import send_async_email


class NotificationCreateAPIView(CreateAPIView):
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        notification = serializer.save()

        recipient_list = get_recipient_list(serializer.validated_data['users'])
        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']

        send_async_email.delay(subject, message, settings.EMAIL_HOST_USER, recipient_list,)

