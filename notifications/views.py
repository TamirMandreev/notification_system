from rest_framework.generics import CreateAPIView

from notifications.serializers import NotificationSerializer


class NotificationCreateAPIView(CreateAPIView):
    serializer_class = NotificationSerializer