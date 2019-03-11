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
        artists = self.upsert_artists(artists_data)

        for artist in artists:
            releases_data = self.fetch_artist_releases(artist)
            self.upsert_artist_releases(artist, releases_data)


    def fetch_artists(self):
        artists = []
        all_artists_loaded = False
        url = f"https://api.deezer.com/user/{self.integration_user_id}/artists"

        while not all_artists_loaded:
            response = requests.get(url).json()
            artists += response['data']
            if response.get('next'):
                url = response['next']
            else:
                all_artists_loaded = True

        return artists


    def upsert_artists(self, artists):
        for artist in artists:
            find_by = {"integration": self.integration, "integration_artist_id": artist["id"]}
            update = {"name": artist["name"]}
            if Artist.objects.filter(**find_by).exists():
                Artist.objects.filter(**find_by).update(**update)
            else:
                Artist.objects.create(**update, **find_by)

        return(self.integration.artist_set.all())


    def fetch_artist_releases(self, artist):
        releases = []
        all_releases_loaded = False
        artist_id = artist.integration_artist_id
        url = f"https://api.deezer.com/artist/{artist_id}/albums"

        while not all_releases_loaded:
            response = requests.get(url).json()
            releases += response['data']
            if response.get('next'):
                url = response['next']
            else:
                all_releases_loaded = True
            time.sleep(0.1)

        return(releases)


    def upsert_artist_releases(self, artist, releases):
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
            if Release.objects.filter(**find_by).exists():
                Release.objects.filter(**find_by).update(**update)
            else:
                Release.objects.create(**update, **find_by)
