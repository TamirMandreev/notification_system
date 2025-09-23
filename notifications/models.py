from django.db import models


class Notification(models.Model):
    users = models.JSONField()
    subject = models.CharField(max_length=255)
    message = models.TextField()


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    number = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class EmailSendStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_attempted = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)

