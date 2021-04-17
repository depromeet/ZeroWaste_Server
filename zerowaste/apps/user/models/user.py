from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.db import models


class User(SoftDeleteModelBase):
    # level은 그냥 1부터 계속 쌓으면 될거같아
    # class Level:
    #     INIT = 0
    #     levels = (
    #         (INIT, 'init'),
    #     )

    name = models.CharField(max_length=8)
    nickname = models.CharField(max_length=10)
    level = models.SmallIntegerField('level', default=1)
    reported_counts = models.SmallIntegerField(default=0)
    is_notify = models.BooleanField(default=True)
