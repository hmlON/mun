from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from integrations.models import Release
from notifications.forms import EmailNotificationForm, TelegramNotificationForm

@login_required
def index(request):
    user_id = request.user.id

    integration = request.user.integration_set.get(identifier='spotify')
    releases = Release.objects.filter(artist__integration_id=integration.id).order_by('-date')[:200]
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

@login_required
def artist(request, name):
    integration = request.user.integration_set.get(identifier='spotify')
    artist = integration.artist_set.get(name__iexact=name)
    releases = artist.release_set.all().order_by('-date')

    context = {'artist': artist, 'releases': releases}
    return render(request, 'artists/show.html', context)

@staff_member_required
def admin_dashboard(request):
    from django.contrib.auth.models import User
    from integrations.models import Integration
    from notifications.models import Notification
    from django.db.models import Count
    import matplotlib.pyplot as plt
    import mpld3

    total_users_count = User.objects.count()

    total_integrations_count = Integration.objects.count()
    integrations_by_identifier = Integration.objects.values('identifier').annotate(count=Count('identifier'))

    x = [integration['count'] for integration in integrations_by_identifier]
    labels = [integration['identifier'] for integration in integrations_by_identifier]
    fig = plt.figure(figsize=(5, 5))
    positions = range(len(x))
    plt.bar(positions, x, color='lightblue')
    plt.xticks(positions, labels)
    integrations_by_identifier_chart = mpld3.fig_to_html(fig)

    total_notifications_count = Notification.objects.count()
    notifications_by_identifier = Notification.objects.values('channel').annotate(count=Count('channel'))

    x = [notification['count'] for notification in notifications_by_identifier]
    labels = [notification['channel'] for notification in notifications_by_identifier]
    fig = plt.figure(figsize=(5, 5))
    positions = range(len(x))
    plt.bar(positions, x, color='lightblue')
    plt.xticks(positions, labels)
    notifications_by_identifier_chart = mpld3.fig_to_html(fig)

    context = {
        'total_users_count': total_users_count,
        'total_integrations_count': total_integrations_count,
        'integrations_by_identifier_chart': integrations_by_identifier_chart,
        'total_notifications_count': total_notifications_count,
        'notifications_by_identifier_chart': notifications_by_identifier_chart,
        # 'fig': g,
    }
    return render(request, 'admin/dashboard.html', context)

    # import matplotlib.pyplot as plt, mpld3
    # from django.http import HttpResponse

    # fig = plt.figure()
    # plt.plot([1,2,3,4])
    # g = mpld3.fig_to_html(fig)
    # return HttpResponse(g)
