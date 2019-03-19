from .base_fetcher import BaseFetcher
from django.shortcuts import render
from integrations.models import Artist, Release
import datetime
from dateutil.parser import parse

class DeezerFetcher(BaseFetcher):
    def integration_identifier(self):
        return('deezer')


    def fetch_artists(self):
        integration_user_id = self.integration.integration_user_id
        url = f"https://api.deezer.com/user/{integration_user_id}/artists"

        return(
            self.fetch_data(url,
                path_to_data=['data'],
                path_to_next=['next']
            )
        )


    def update_or_create_artists(self, artists):
        for artist in artists:
            find_by = {"integration": self.integration, "integration_artist_id": artist["id"]}
            update = {"name": artist["name"]}
            Artist.objects.update_or_create(**find_by, defaults=update)

        return(self.integration.artist_set.all())


    def fetch_artist_releases(self, artist):
        integration_artist_id = artist.integration_artist_id
        url = f"https://api.deezer.com/artist/{integration_artist_id}/albums"

        return(
            self.fetch_data(url,
                path_to_data=['data'],
                path_to_next=['next']
            )
        )


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
                "explicit": release["explicit_lyrics"],
            }
            Release.objects.update_or_create(**find_by, defaults=update)
