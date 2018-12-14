from django.contrib.auth.models import User
from django.shortcuts import render
from integrations.models import Artist, Release
import requests

class DeezerFetcher():
    def fetch(user_id):
        user = User.objects.get(pk=user_id)

        # get integration
        integration = user.integration_set.get(identifier='deezer')
        user_id = integration.integration_user_id

        # load all artists
        artists = []
        all_artists_loaded = False
        url = f"https://api.deezer.com/user/{user_id}/artists"

        while not all_artists_loaded:
            response = requests.get(url).json()
            artists += response['data']
            if response.get('next'):
                url = response['next']
            else:
                all_artists_loaded = True

        # save or update loaded artists
        for artist in artists:
            find_by = {"integration": integration, "integration_artist_id": artist["id"]}
            update = {"name": artist["name"]}
            if Artist.objects.filter(**find_by).exists():
                Artist.objects.filter(**find_by).update(**update)
            else:
                Artist.objects.create(**update, **find_by)

        artists = integration.artist_set.all()

        for artist in artists:
            # load releases
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

            # save or update releases
            for release in releases:
                find_by = {"artist": artist, "integration_release_id": release["id"]}
                update = {
                    "title": release["title"],
                    "cover_url": release["cover"],
                    "date": release["release_date"],
                    "release_type": release["type"],
                }
                if Release.objects.filter(**find_by).exists():
                    Release.objects.filter(**find_by).update(**update)
                else:
                    Release.objects.create(**update, **find_by)
