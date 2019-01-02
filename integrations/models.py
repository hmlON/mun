from django.db import models
from django.contrib.auth.models import User

class Integration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=50)
    access_token = models.CharField(max_length=256, null=True)
    refresh_token = models.CharField(max_length=256, null=True)
    integration_user_id = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.identifier} ({self.id})"


class Artist(models.Model):
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    integration_artist_id = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

class Release(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    integration_release_id = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256)
    cover_url = models.CharField(max_length=256)
    date = models.DateField()
    release_type = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.id})"
