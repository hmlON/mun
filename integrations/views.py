from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from integrations.models import Release
from integrations.music_service_fetchers.deezer_fetcher import DeezerFetcher

@login_required
def index(request):
    user_id = request.user.id

    integration = request.user.integration_set.get(identifier='spotify')
    releases = Release.objects.filter(artist__integration_id=integration.id).order_by('-date')
    context = {'user': request.user, 'releases': releases}
    return render(request, 'releases/index.html', context)
