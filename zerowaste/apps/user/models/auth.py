from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.db import models


class Auth(SoftDeleteModelBase):
    class LoginType:
        Kakao = 0
        Apple = 1
        types = (
            (Kakao, 'kakao'),
            (Apple, 'apple'),
        )

    email = models.CharField(max_length=100, unique=True)
    user_id = models.BigAutoField()
    social_token = models.CharField(max_length=150)
    login_type = models.SmallIntegerField('state', choices=LoginType.types)
    token = models.CharField(max_length=200)
