from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.core.validators import MinLengthValidator
from django.db import models


class Certification(SoftDeleteModelBase):
    class Percieved_difficulty(models.TextChoices):
        HARD = 'hard'
        MEDIUM = 'medium'
        EASY = 'easy'
        FIT = 'fit'

    name = models.CharField(max_length=50, default="")
    mission_id = models.ForeignKey("Mission", related_name="certified_mission", on_delete=models.DO_NOTHING,
                                   db_column="mission_id")
    owner = models.ForeignKey("user.User", related_name="certified_user", on_delete=models.DO_NOTHING,
                                db_column="owner")
    content = models.CharField(validators=[MinLengthValidator(10)], max_length=1500)
    img_url = models.CharField(max_length=200)
    isPublic = models.BooleanField(default=True)
    percieved_difficulty = models.CharField('percieved_difficulty', max_length=10,
                                            choices=Percieved_difficulty.choices)