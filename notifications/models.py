from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=50)
    last_sent_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
    connect_token = models.CharField(max_length=64, null=True)
    channel_id = models.CharField(max_length=64, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel} ({self.id})"
