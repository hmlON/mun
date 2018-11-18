from django.shortcuts import render
from integrations.models import Artist, Release
import requests
import logging
logger = logging.getLogger(__name__)

def index(request):
    # get integration
    integration = request.user.integration_set.get(identifier='deezer')
    user_id = integration.integration_user_id

    # load all artists
    # TODO: use next param instead of loop
    artists = []
    all_artists_loaded = False
    index = 0
    limit = 50

    while not all_artists_loaded:
        url = f"https://api.deezer.com/user/{user_id}/artists?index={index}&limit={limit}"
        current_request_artists = requests.get(url).json()['data']
        logger.info(f"Getting data from {url}")
        artists += current_request_artists
        index += limit
        all_artists_loaded = len(current_request_artists) < limit

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
        index = 0
        limit = 50
        artist_id = artist.integration_artist_id

        while not all_releases_loaded:
              url = f"https://api.deezer.com/artist/{artist_id}/albums?index={index}&limit={limit}"
              current_request_releases = requests.get(url).json()['data']
              logger.info(f"Getting data from {url}")
              releases += current_request_releases
              index += limit
              all_releases_loaded = len(current_request_artists) < limit

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

    # render
    releases = Release.objects.all().order_by('-date')
    context = {'user': request.user, 'releases': releases}
    return render(request, 'artists/index.html', context)
