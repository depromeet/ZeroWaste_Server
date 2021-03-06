from apps.core.models.model_base import ModelBase
from django.db import models


class Participation(ModelBase):
    class Status(models.TextChoices):
        READY = 'ready'
        PARTICIPATED = 'participated'
        SUCCESS = 'success'
        FAILURE = 'failure'

    mission = models.ForeignKey("Mission", related_name="participated_mission", on_delete=models.CASCADE,
                                   db_column="mission")
    owner = models.ForeignKey("user.User", related_name="participated_user", on_delete=models.CASCADE,
                                db_column="owner")
    status = models.CharField('status', max_length=15, choices=Status.choices, default=Status.READY)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_cron_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == Participation.Status.SUCCESS:
            self.mission.update_successful_count()
        else:
            self.mission.update_in_progress_count()
