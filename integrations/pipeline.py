from integrations.models import Integration

def save_integration(backend, user, response, *args, **kwargs):
    if backend.name == 'spotify':
        access_token        = response['access_token']
        refresh_token       = response['refresh_token']
        integration_user_id = response['id']
    elif backend.name == 'deezer':
        access_token        = None
        refresh_token       = None
        integration_user_id = response['id']

    if Integration.objects.filter(user=user, identifier=backend.name).exists():
        Integration.objects.filter(user=user, identifier=backend.name).update(
            access_token=access_token,
            refresh_token=refresh_token,
            integration_user_id=integration_user_id,
        )
    else:
        Integration.objects.create(
            user=user,
            identifier=backend.name,
            access_token=access_token,
            refresh_token=refresh_token,
            integration_user_id=integration_user_id,
        )
