from django.db import models


class Notification(models.Model):
    users = models.JSONField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
