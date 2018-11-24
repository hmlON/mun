from django.shortcuts import render
from integrations.models import Release
from integrations.music_service_fetchers.deezer_fetcher import DeezerFetcher

def index(request):
    user_id = request.user.id

    DeezerFetcher.fetch(user_id)

    releases = Release.objects.all().order_by('-date')
    context = {'user': request.user, 'releases': releases}
    return render(request, 'releases/index.html', context)
