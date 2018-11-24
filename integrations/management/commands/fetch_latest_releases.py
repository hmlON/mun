from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from integrations.music_service_fetchers.deezer_fetcher import DeezerFetcher

class Command(BaseCommand):
    help = 'Fetches latest releases'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            self.stdout.write(self.style.SUCCESS(f'starting fetching for {user}'))
            DeezerFetcher.fetch(user.id)
            self.stdout.write(self.style.SUCCESS(f'finished fetching for {user}'))
