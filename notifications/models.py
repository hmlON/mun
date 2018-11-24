from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=50)
    last_sent_at = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
