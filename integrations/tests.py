from django.test import TestCase
from django.contrib.auth.models import User
from .models import Integration, Artist, Release
from .music_service_fetchers.spotify_fetcher import SpotifyFetcher
from .music_service_fetchers.deezer_fetcher import DeezerFetcher

class SpotifyFetcherTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        integration = Integration.objects.create(
            user=self.user,
            identifier='spotify',
            access_token='BQC8Jk4RdHSvz-plmoKca07gwMX98NaHzd0WTtVJp2W9rcOO922LitYEgCVUNbo27uORR7NEP8e8otqTLJFl27WEsjt9rVy1SERjYKcU9HblsRINsR3Zbww13q2bxHakSn9HFPVTpFYsSGua5sSk',
            refresh_token='AQDZb34FytndcQAkRnAHmnjqqA-Baz8f-uF6SbTy8wQEhCVGnFrRx0jZUGLKVKCO8dNEGL13Gzsi1vQd4XKU9JiiTHRxocy8qWgFVv7R0CKRudXPOVLGoIFTV2BtaABwdi7eQg',
            integration_user_id='hmlon',
        )

    def test_spotify_fetcher_creates_releases(self):
        self.assertEqual(Release.objects.count(), 0)
        self.assertEqual(Artist.objects.count(), 0)

        SpotifyFetcher.fetch(self.user.id)

        self.assertNotEqual(Artist.objects.count(), 0)
        self.assertNotEqual(Release.objects.count(), 0)

class DeezerFetcherTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        Integration.objects.create(
            user=self.user,
            identifier='deezer',
            integration_user_id='700513741',
        )

    def test_deezer_fetcher_creates_releases(self):
        self.assertEqual(Release.objects.count(), 0)
        self.assertEqual(Artist.objects.count(), 0)

        DeezerFetcher.fetch(self.user.id)

        self.assertNotEqual(Artist.objects.count(), 0)
        self.assertNotEqual(Release.objects.count(), 0)
