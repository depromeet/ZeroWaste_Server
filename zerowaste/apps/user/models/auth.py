from apps.core.models.soft_delete_model_base import ModelBase
from django.db import models


class Auth(ModelBase):
    class LoginType:
        Kakao = 0
        Apple = 1
        types = (
            (Kakao, 'kakao'),
            (Apple, 'apple'),
        )

    identifier = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    #TODO: user_id -> user
    user_id = models.ForeignKey("User", related_name="auth_user", on_delete=models.CASCADE, db_column="user_id")
    social_token = models.CharField(max_length=150)
    login_type = models.SmallIntegerField('state', choices=LoginType.types)
    token = models.CharField(max_length=300)

