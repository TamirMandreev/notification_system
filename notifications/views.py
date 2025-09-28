from rest_framework.generics import CreateAPIView

from notifications.serializers import NotificationSerializer
from notifications.services import (create_users, delete_objects,
                                    generate_notification_report,
                                    send_email_message, send_sms_message,
                                    send_telegram_message)


class NotificationCreateAPIView(CreateAPIView):
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        serializer.save()

        # Извлечь тему и текст сообщения
        subject = serializer.validated_data["subject"]
        message = serializer.validated_data["message"]

        # Создать пользователей
        create_users(serializer.validated_data["users"])

        # Отправить каждому пользователю письмо на эл. почту
        send_email_message(subject, message)
        # Кому не получилось отправить на эл. почту, отправить в Telegram
        send_telegram_message(subject, message)
        # Кому не получилось отправить в Telegram, отправить смс
        send_sms_message(message)
        # Создать отчет
        generate_notification_report()
        # Удалить созданные объекты
        delete_objects()
