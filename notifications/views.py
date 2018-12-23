from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
from secrets import token_urlsafe
from django.views.decorators.csrf import csrf_exempt
import json
from notifications.models import Notification
import requests
import os

@login_required
def create(request):
    notification, _created = request.user.notification_set.get_or_create(
      channel='telegram',
      defaults={'connect_token': token_urlsafe(8)}
    )

    bot_url = 'https://www.telegram.me/music_notification_bot'
    return redirect(f'{bot_url}?start={notification.connect_token}')

@csrf_exempt
def callback(request):
    body = json.loads(request.body)
    text = body['message']['text'].split(' ')
    token = None
    if len(text) > 1:
        token = text[1]

    bot_key = os.environ.get('TELEGRAM_API_KEY')
    chat_id = body['message']['chat']['id']

    try:
        notification = Notification.objects.get(channel='telegram', connect_token=token)
        notification.channel_id = chat_id
        notification.save()

        text = "Welcome to the MuN"
        send_message_url = f'https://api.telegram.org/bot{bot_key}/sendMessage?chat_id={chat_id}&text={text}'
        requests.post(send_message_url)

        return HttpResponse()
    except Notification.DoesNotExist:
        text = "Sorry, seems like the MuN is too far..."
        send_message_url = f'https://api.telegram.org/bot{bot_key}/sendMessage?chat_id={chat_id}&text={text}'
        requests.post(send_message_url)

        return HttpResponse()
