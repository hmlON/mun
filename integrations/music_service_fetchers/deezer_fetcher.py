from django.contrib.auth.models import User
from django.shortcuts import render
from integrations.models import Artist, Release
import requests
import datetime
from dateutil.parser import parse
import time

class DeezerFetcher():
    def __init__(self, user_id):
        user = User.objects.get(pk=user_id)
        self.integration = user.integration_set.get(identifier='deezer')
        self.integration_user_id = self.integration.integration_user_id

    def fetch(self):
        artists_data = self.fetch_artists()
        artists = self.update_or_create_artists(artists_data)

        for artist in artists:
            releases_data = self.fetch_artist_releases(artist)
            self.update_or_create_artist_releases(artist, releases_data)


    def fetch_artists(self):
        integration_user_id = self.integration.integration_user_id
        url = f"https://api.deezer.com/user/{integration_user_id}/artists"
        return(self.fetch_data(url))


    def update_or_create_artists(self, artists):
        for artist in artists:
            find_by = {"integration": self.integration, "integration_artist_id": artist["id"]}
            update = {"name": artist["name"]}
            Artist.objects.update_or_create(**find_by, defaults=update)

        return(self.integration.artist_set.all())


    def fetch_artist_releases(self, artist):
        integration_artist_id = artist.integration_artist_id
        url = f"https://api.deezer.com/artist/{integration_artist_id}/albums"
        return(self.fetch_data(url))


    def update_or_create_artist_releases(self, artist, releases):
        for release in releases:
            try:
                release_date = parse(release["release_date"])
            except ValueError:
                release_date = str(datetime.date.today())

            find_by = {"artist": artist, "integration_release_id": release["id"]}
            update = {
                "title": release["title"],
                "cover_url": release["cover"],
                "date": release_date,
                "release_type": release["type"],
                "integration_url": release["link"],
            }
            Release.objects.update_or_create(**find_by, defaults=update)

    def fetch_data(self, url):
        data = []
        all_data_loaded = False

        while not all_data_loaded:
            response = requests.get(url).json()
            data += response['data']
            if response.get('next'):
                url = response['next']
            else:
                all_data_loaded = True
            time.sleep(0.1)

        return(data)
