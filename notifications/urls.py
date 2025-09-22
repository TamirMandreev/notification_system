from django.urls import path

from notifications import views
from notifications.apps import NotificationsConfig

app_name = NotificationsConfig.name

urlpatterns = [
    path('create/', views.NotificationCreateAPIView.as_view(), name="create"),
]