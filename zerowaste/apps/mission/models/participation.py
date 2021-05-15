from apps.core.models.model_base import ModelBase
from django.db import models


class Participation(ModelBase):
    class Status(models.TextChoices):
        READY = 'ready' # 인증 준비중
        PARTICIPATED = 'participated' # 하나라도 인증을 올림
        SUCCESS = 'success'
        FAILURE = 'failure'

    mission_id = models.ForeignKey("Mission", related_name="participated_mission", on_delete=models.CASCADE,
                                   db_column="mission_id")
    owner = models.ForeignKey("user.User", related_name="participated_user", on_delete=models.CASCADE,
                                db_column="owner")
    status = models.CharField('status', max_length=15, choices=Status.choices, default=Status.READY)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()