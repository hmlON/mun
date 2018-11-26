from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from integrations.music_service_fetchers.deezer_fetcher import DeezerFetcher
from integrations.models import Release
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Fetches latest releases'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            self.stdout.write(self.style.SUCCESS(f'starting fetching for {user}'))
            # DeezerFetcher.fetch(user.id)
            self.stdout.write(self.style.SUCCESS(f'finished fetching for {user}'))

            integration = user.integration_set.get(identifier='deezer')
            notification = user.notification_set.get(channel='email')

            # new_since = notification.last_sent_at
            import datetime
            new_since = datetime.date.today() - datetime.timedelta(days=30)

            new_releases = Release.objects.filter(
              artist__integration_id=integration.id,
              date__gte=new_since
            ).order_by('-date')

            if new_releases.exists():
              self.stdout.write(self.style.SUCCESS(f'sending an email for {user} to {user.email} '))

              releases_text = [f'{release.date}: {release.artist.name} - {release.title}' for release in new_releases]
              intro_text = 'Here are latest music releases that you have not seen before:'
              email_text = '\n'.join([intro_text] + releases_text)

              send_mail(
                  'New music releases',
                  email_text,
                  'nik.kholin@gmail.com',
                  [user.email],
                  fail_silently=False,
              )
            else:
              self.stdout.write(self.style.SUCCESS(f'no new releases {user}'))
