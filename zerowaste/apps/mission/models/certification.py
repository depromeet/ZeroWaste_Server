from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.db import models


class Certification(SoftDeleteModelBase):
    name = models.CharField(max_length=50, default="")
    mission_id = models.ForeignKey("Mission", related_name="certified_mission", on_delete=models.DO_NOTHING,
                                   db_column="mission_id")
    owner = models.ForeignKey("user.User", related_name="certified_user", on_delete=models.DO_NOTHING,
                                db_column="owner")
    content = models.CharField(max_length=1500)
    image = models.CharField(max_length=200)
    isPublic = models.BooleanField(default=True)