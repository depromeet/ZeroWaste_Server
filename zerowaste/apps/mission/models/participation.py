from apps.core.models.model_base import ModelBase
from django.db import models


class Mission(ModelBase):
    class Status:
        READY = 0
        PROGRESS = 1
        COMPLETE = 2
        status = (
            (READY, 'ready'),
            (PROGRESS, 'progress'),
            (COMPLETE, 'complete'),
        )

    mission_id = models.ForeignKey("Mission", related_name="participated_mission", on_delete=models.CASCADE,
                                   db_column="mission_id")
    user_id = models.ForeignKey("user.User", related_name="participated_user", on_delete=models.CASCADE,
                                db_column="user_id")
    status = models.SmallIntegerField('status', choices=Status.status, default=Status.READY)
