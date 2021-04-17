from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.db import models


class User(SoftDeleteModelBase):
    class Level:
        INIT = 0
        levels = (
            (INIT, 'init'),
        )

    name = models.CharField(max_length=8)
    nickname = models.CharField(max_length=10)
    level = models.SmallIntegerField('state', choices=Level.levels, default=Level.INIT)
    reported_counts = models.SmallIntegerField(default=0)
    is_notify = models.BooleanField(default=True)
