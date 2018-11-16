from django.shortcuts import render
from integrations.models import Artist
import requests

def index(request):
    # get integration
    integration = request.user.integration_set.get(identifier='deezer')
    user_id = integration.integration_user_id

    # load all artists
    artists = []
    all_artists_loaded = False
    index = 0
    limit = 50

    while not all_artists_loaded:
      url = f"https://api.deezer.com/user/{user_id}/artists?index={index}&limit={limit}"
      current_request_artists = requests.get(url).json()['data']
      artists += current_request_artists
      index += limit
      all_artists_loaded = len(current_request_artists) < limit

    # save or update loaded artists
    for artist in artists:
        find_by = {"integration": integration, "integration_artist_id": artist["id"]}
        if Artist.objects.filter(**find_by).exists():
            Artist.objects.filter(**find_by).update(name=artist["name"])
        else:
            Artist.objects.create(name=artist["name"], **find_by)

    # render
    context = {'user': request.user, 'artists': integration.artist_set.all()}
    return render(request, 'artists/index.html', context)
