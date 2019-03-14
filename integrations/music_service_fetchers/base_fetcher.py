import abc
from django.contrib.auth.models import User

class BaseFetcher():
    def __init__(self, user_id):
        user = User.objects.get(pk=user_id)
        self.integration = user.integration_set.get(identifier=self.integration_identifier())

    @abc.abstractmethod
    def integration_identifier(self):
        return()

    def fetch(self):
        self.activate_integration()

        artists_data = self.fetch_artists()
        artists = self.update_or_create_artists(artists_data)

        for artist in artists:
            releases_data = self.fetch_artist_releases(artist)
            self.update_or_create_artist_releases(artist, releases_data)

    def activate_integration(self):
        return()

    @abc.abstractmethod
    def fetch_artists(self):
        return()

    @abc.abstractmethod
    def update_or_create_artists(self):
        return()

    @abc.abstractmethod
    def fetch_artist_releases(self):
        return()

    @abc.abstractmethod
    def update_or_create_artist_releases(self):
        return()
