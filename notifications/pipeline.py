from notifications.models import Notification

def create_default_notifications(backend, user, response, *args, **kwargs):
    if not Notification.objects.filter(user=user, channel="email").exists():
        Notification.objects.create(user=user, channel="email")
