from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def delete(request):
    request.user.delete()
    # integration = request.user.integration_set.get(identifier='spotify')
    # releases = Release.objects.filter(artist__integration_id=integration.id).order_by('-date')
    # context = {'user': request.user, 'releases': releases}
    return redirect('/')
