from integrations.models import Integration

def save_integration(backend, user, response, *args, **kwargs):
    if backend.name == 'spotify':
        refresh_token       = response['refresh_token']
        integration_user_id = None
    elif backend.name == 'deezer':
        refresh_token       = None
        integration_user_id = response['id']

    if Integration.objects.filter(user=user, identifier=backend.name).exists():
        Integration.objects.filter(user=user, identifier=backend.name).update(
            refresh_token=refresh_token,
            integration_user_id=integration_user_id,
        )
    else:
        Integration.objects.create(
            user=user,
            identifier=backend.name,
            refresh_token=refresh_token,
            integration_user_id=integration_user_id,
        )
