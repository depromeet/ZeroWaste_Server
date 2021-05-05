from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from apps.core.models.soft_delete_model_base import ModelBase
from apps.core.utils.tools import id_generator
from apps.user.models.auth import Auth

class UserManager(BaseUserManager):
    def create_user(self, nickname, is_active=True, **extra_fields):
        if not nickname:
            raise ValueError("User must have an nickname")

        user = self.model(nickname=nickname, **extra_fields)
        user.is_admin = False
        user.is_staff = False
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None):
        user = self.model()
        user.nickname = nickname
        user.username = nickname
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser, ModelBase):
    first_name = None
    last_name = None
    username = None

    nickname = models.CharField(max_length=10, unique=True)
    level = models.SmallIntegerField('level', default=1)
    is_notify = models.BooleanField(default=True)
    description = models.CharField(max_length=100, unique=True)
    # reported_counts = models.SmallIntegerField(default=0)

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def delete(self, *args, **kwargs):
        self.nickname = id_generator()
        self.level = 0
        try:
            auth = Auth.objects.get(user_id=self.id)
            auth.delete()
        except:
            pass
        self.save()
