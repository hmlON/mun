from django.shortcuts import render
from integrations.models import Release
from integrations.music_service_fetchers.deezer_fetcher import DeezerFetcher

def index(request):
    user_id = request.user.id

    # DeezerFetcher.fetch(user_id)

    integration = request.user.integration_set.get(identifier='spotify')
    releases = Release.objects.filter(artist__integration_id=integration.id).order_by('-date')
    context = {'user': request.user, 'releases': releases}
    return render(request, 'releases/index.html', context)
