from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.db import models
from django_mysql.models import ListCharField


class Mission(SoftDeleteModelBase):
    class Place(models.TextChoices):
        ETC = 'etc'
        KITCHEN = 'kitchen'
        BATHROOM = 'bathroom'
        CAFE = 'cafe'
        RESTAURANT = 'restaurant'
        OUTSIDE = 'outside'

    class Difficulty(models.TextChoices):
        VERY_EASY = 'very_easy'
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'
        EXTRA_HARD = 'extra_hard'

    name = models.CharField(max_length=50, default="")
    owner = models.ForeignKey("user.User", related_name="mission_creater", on_delete=models.DO_NOTHING,
                                   db_column="owner")  # CASCADE 되면 안됨
    place = models.CharField(max_length=10,
                             choices=Place.choices,
                             default=Place.ETC)
    theme = ListCharField(
        base_field=models.CharField(max_length=10),
        size=10,
        max_length=(10 * 11),
        default=['refuse', 'reduce', 'reuse', 'recycle', 'rot']
    )
    difficulty = models.CharField('difficulty', max_length=10, choices=Difficulty.choices, default=Difficulty.VERY_EASY)
    logo_img_url = models.CharField(max_length=200)
    icon_img_url = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    is_public = models.BooleanField(default=True)
    sentence_for_cheer = models.CharField(max_length=50, default="")

