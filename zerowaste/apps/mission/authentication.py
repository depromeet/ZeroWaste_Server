from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from apps.core.exceptions import BadRequest


class User:
    def __init__(self):
        self.is_authenticated = True


class BatchAuthentication(BaseAuthentication):
    def authenticate(self, request):
        batch_key = request.META.get('HTTP_AUTHORIZATION')
        if not batch_key:
            raise BadRequest("batch key is empty")
        if batch_key != settings.BATCH_KEY:
            raise BadRequest("batch key is invalid")
        return User(), True
