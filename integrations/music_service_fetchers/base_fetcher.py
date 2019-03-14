import abc
from django.contrib.auth.models import User

class BaseFetcher():
    def __init__(self, user_id):
        user = User.objects.get(pk=user_id)
        self.integration = user.integration_set.get(identifier=self.integration_identifier())

    @abc.abstractmethod
    def integration_identifier(self):
        return()
