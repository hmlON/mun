from .base_fetcher import BaseFetcher
from integrations.models import Artist, Release
from spotipy.oauth2 import SpotifyOAuth
import datetime
import os
from dateutil.parser import parse

class SpotifyFetcher(BaseFetcher):
    def integration_identifier(self):
        return('spotify')


    def activate_integration(self):
        client_id = os.environ.get('SPOTIFY_KEY', '')
        client_secret = os.environ.get('SPOTIFY_SECRET', '')
        sp_oauth = SpotifyOAuth(client_id, client_secret, None)
        token_info = sp_oauth.refresh_access_token(self.integration.refresh_token)

        self.integration.access_token = token_info['access_token']
        self.integration.refresh_token = token_info['refresh_token']
        self.integration.save()


    def fetch_artists(self):
        token = self.integration.access_token
        limit = 50
        url = f"https://api.spotify.com/v1/me/following?type=artist&limit={limit}&access_token={token}"

        return(
            self.fetch_data(url,
                path_to_data=['artists', 'items'],
                path_to_next=['artists', 'next']
            )
        )


    def update_or_create_artists(self, artists):
        for artist in artists:
            find_by = {"integration": self.integration, "integration_artist_id": artist["id"]}
            update = {"name": artist["name"]}
            Artist.objects.update_or_create(**find_by, defaults=update)

        return(self.integration.artist_set.all())


    def fetch_artist_releases(self, artist):
        artist_id = artist.integration_artist_id
        token = self.integration.access_token
        limit = 50
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit={limit}&access_token={token}"

        return(
            self.fetch_data(url,
                path_to_data=['items'],
                path_to_next=['next']
            )
        )


    def update_or_create_artist_releases(self, artist, releases):
        for release in releases:
            find_by = {"artist": artist, "integration_release_id": release["id"]}

            try:
                release_date = parse(release['release_date'])
            except ValueError:
                release_date = str(datetime.date.today())

            cover_url = release['images']
            if len(cover_url) > 0:
                cover_url = max(release['images'], key=lambda image: image['width'])['url']
            else:
                cover_url = ''

            update = {
                "title": release["name"],
                "cover_url": cover_url,
                "date": release_date,
                "release_type": release["album_type"],
                "integration_url": release['external_urls']['spotify'],
            }
            Release.objects.update_or_create(**find_by, defaults=update)
