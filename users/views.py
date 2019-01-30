from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def delete(request):
    request.user.delete()
    return redirect('/')
