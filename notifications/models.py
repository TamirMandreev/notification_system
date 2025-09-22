from django.db import models

from django.contrib.postgres.fields import ArrayField

class Notification(models.Model):
    users = ArrayField(models.CharField(max_length=255), default=list, size=4)
    subject = models.CharField(max_length=255)
    body = models.TextField()
