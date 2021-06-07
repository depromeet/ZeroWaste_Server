from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.db import models
from django_mysql.models import ListCharField
from apps.mission.models.likes import MissionLike
from apps.mission.models.participation import Participation


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
    banner_img_urls = ListCharField(
        base_field=models.URLField(max_length=150),
        size=3,
        max_length=(3 * 151),
        default=[]
    )
    content = models.CharField(max_length=1000)
    is_public = models.BooleanField(default=True)
    sentence_for_cheer = models.CharField(max_length=50, default="")

    likes_count = models.IntegerField(default=0)
    successful_count = models.IntegerField(default=0)
    in_progress_count = models.IntegerField(default=0)

    def update_likes_count(self):
        self.likes_count = MissionLike.objects.filter(mission=self).count()
        self.save()

    def update_successful_count(self):
        self.successful_count = Participation.objects.filter(mission=self, status=Participation.Status.SUCCESS).count()
        self.save()

    def update_in_progress_count(self):
        user_in_progress_counts = Participation.objects.filter(mission=self, status=Participation.Status.READY).count()
        self.in_progress_count = user_in_progress_counts
        self.save()
