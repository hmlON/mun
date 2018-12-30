from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from integrations.models import Release
from notifications.forms import EmailNotificationForm, TelegramNotificationForm

@login_required
def index(request):
    user_id = request.user.id

    integration = request.user.integration_set.get(identifier='spotify')
    releases = Release.objects.filter(artist__integration_id=integration.id).order_by('-date')
    context = {'user': request.user, 'releases': releases}
    return render(request, 'releases/index.html', context)

@login_required
def settings(request):
    notifications = request.user.notification_set

    email_notification = notifications.get(channel="email")
    channel_id = email_notification.channel_id or request.user.email
    enabled = email_notification.enabled
    email_notification_form_data = {
        'channel_id': channel_id,
        'enabled': enabled,
        'notification_id': email_notification.id,
    }
    email_notification_form = EmailNotificationForm(email_notification_form_data)

    telegram_notification_form = None
    if notifications.filter(channel="telegram").exists():
        telegram_notification = notifications.get(channel="telegram")
        enabled = telegram_notification.enabled
        telegram_notification_form_data = {
            'enabled': enabled,
            'notification_id': telegram_notification.id,
        }
        telegram_notification_form = TelegramNotificationForm(telegram_notification_form_data)

    context = {
        'user': request.user,
        'email_notification_form': email_notification_form,
        'telegram_notification_form': telegram_notification_form,
    }
    return render(request, 'settings/index.html', context)
