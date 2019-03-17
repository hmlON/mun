import abc
from django.contrib.auth.models import User
import requests
from dict_digger import dig
import time
from retryable import retry

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

    @retry()
    def fetch_data(self, url, path_to_data, path_to_next):
        token = self.integration.access_token
        data = []
        all_data_loaded = False

        while not all_data_loaded:
            response = requests.get(url).json()
            if response:
                data += dig(response, *path_to_data)
            else:
                return data

            next_url = dig(response, *path_to_next)
            if next_url:
                if token:
                    url = next_url + f"&access_token={token}"
                else:
                    url = next_url
            else:
                all_data_loaded = True
            time.sleep(0.1)

        return(data)
