from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from integrations.music_service_fetchers.deezer_fetcher import DeezerFetcher
from integrations.music_service_fetchers.spotify_fetcher import SpotifyFetcher
from integrations.models import Release
from django.core.mail import send_mail
import datetime
import os
import requests

import bugsnag
import logging
from bugsnag.handlers import BugsnagHandler
bugsnag.configure(
  api_key = os.environ.get('BUGSNAG_API_KEY'),
  project_root = '../../',
)
logger = logging.getLogger('test.logger')
handler = BugsnagHandler()
handler.setLevel(logging.ERROR)
logger.addHandler(handler)


class Command(BaseCommand):
    help = 'Fetches latest releases'

    def handle(self, *args, **options):
        users = User.objects.all()

        for user in users:
            self.stdout.write(self.style.SUCCESS(f'starting fetching for {user.email}'))

            integration = None
            if user.integration_set.filter(identifier='spotify').exists():
                integration = user.integration_set.get(identifier='spotify')
                SpotifyFetcher(user.id).fetch()
            elif user.integration_set.filter(identifier='deezer').exists():
                integration = user.integration_set.get(identifier='deezer')
                DeezerFetcher(user.id).fetch()

            if not integration:
              continue

            self.stdout.write(self.style.SUCCESS(f'finished fetching for {user.email}'))


            if user.notification_set.filter(channel='email', enabled=True).exists():
                notification = user.notification_set.get(channel='email')
                new_since = notification.last_sent_at
                # new_since = datetime.date.today() - datetime.timedelta(days=7)
                new_releases = Release.objects.filter(
                    artist__integration_id=integration.id,
                    date__gte=new_since,
                    created_at__gte=new_since,
                ).order_by('-date', '-created_at')


                # send an email
                if new_releases.exists():
                    self.stdout.write(self.style.SUCCESS(f'sending an email for {user.email} '))

                    releases_text = [f'{release.date}: {release.artist.name} - {release.title}' for release in new_releases]
                    releases_html = [f'{release.date}: {release.artist.name} - <a href="{release.integration_url}">{release.title}</a>' for release in new_releases]
                    intro_text = 'Here are latest music releases that you have not seen before:'
                    outro_text = 'If you’d like to stop receiving these notifications, please visit the settings page.'
                    text_content = '\n'.join([intro_text] + releases_text + ['\n', '--', outro_text])
                    html_content = '<br>'.join([intro_text] + releases_html + ['\n', '--', outro_text])

                    to = notification.channel_id or user.email

                    send_mail(
                        f'New music releases since {new_since}',
                        text_content,
                        '"MuN: latest releases" <latest.releases@musicnotifier.com>',
                        [to],
                        html_message=html_content,
                        fail_silently=False,
                    )

                    notification.last_sent_at = datetime.datetime.now()
                    notification.save()
                else:
                    self.stdout.write(self.style.SUCCESS(f'no new releases {user.email}'))


            # send a telegram message
            if user.notification_set.filter(channel='telegram', enabled=True).exists():
                notification = user.notification_set.get(channel='telegram')
                new_since = notification.last_sent_at
                # new_since = datetime.date.today() - datetime.timedelta(days=7)
                new_releases = Release.objects.filter(
                    artist__integration_id=integration.id,
                    date__gte=new_since,
                    created_at__gte=new_since,
                ).order_by('-date', '-created_at')

                if new_releases.exists():
                    self.stdout.write(self.style.SUCCESS(f'sending a telegram message for {notification.channel_id} '))

                    releases_text = [
                        f'{release.date}: {release.artist.name} - [{release.title}]({release.integration_url})'
                        for release in new_releases
                    ]
                    intro_text = 'Here are latest music releases that you have not seen before:'
                    text = '\n'.join([intro_text] + releases_text)

                    bot_key = os.environ.get('TELEGRAM_API_KEY')
                    chat_id = notification.channel_id
                    send_message_url = f'https://api.telegram.org/bot{bot_key}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=markdown'
                    requests.post(send_message_url)

                    # update last sent at
                    notification.last_sent_at = datetime.datetime.now()
                    notification.save()
                else:
                    self.stdout.write(self.style.SUCCESS(f'no new releases {notification.channel_id}'))
