from django.db import models


class Notification(models.Model):
    users = models.JSONField()
    subject = models.CharField(max_length=255)
    message = models.TextField()


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    number = models.CharField(max_length=255)
    tg_chat_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email


class EmailSendStatus(models.Model):
    """
    Хранит результаты отправки сообщений по электронной почте
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_attempted = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)


class TelegramSendStatus(models.Model):
    """
    Хранит результаты отправки сообщений в Telegram
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_attempted = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)


class SmsSendStatus(models.Model):
    """
    Хранит результаты отправки смс-сообщений
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_attempted = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
