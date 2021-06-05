from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.core.validators import MinLengthValidator
from django.db import models
from django_mysql.models import ListCharField


class Certification(SoftDeleteModelBase):
    class Percieved_difficulty(models.TextChoices):
        VERY_EASY = 'very_easy'
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'
        EXTRA_HARD = 'extra_hard'

    name = models.CharField(max_length=50, default="")
    mission_id = models.ForeignKey("Mission", related_name="certified_mission", on_delete=models.DO_NOTHING,
                                   db_column="mission_id")
    owner = models.ForeignKey("user.User", related_name="certified_user", on_delete=models.DO_NOTHING,
                                db_column="owner")
    content = models.CharField(validators=[MinLengthValidator(10)], max_length=1500)
    img_urls = ListCharField(
        base_field = models.URLField(max_length=150),
        size = 3,
        max_length =(3*151),
        default=[]
    )
    isPublic = models.BooleanField(default=True)
    percieved_difficulty = models.CharField('percieved_difficulty', max_length=10,
                                            choices=Percieved_difficulty.choices, default="")
