from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.db import models


class Mission(SoftDeleteModelBase):
    class Category:
        REFUSE = 0
        REDUCE = 1
        REUSE = 2
        RECYCLE = 3
        ROT = 4
        category = (
            (REFUSE, 'refuse'),
            (REDUCE, 'reduce'),
            (REUSE, 'reuse'),
            (RECYCLE, 'recycle'),
            (ROT, 'rot'),
        )

    class Difficulty:
        EASY = 0
        MEDIUM = 1
        HARD = 2
        EXTRA_HARD = 3
        difficulty = (
            (EASY, 'easy'),
            (MEDIUM, 'medium'),
            (HARD, 'hard'),
            (EXTRA_HARD, 'extra_hard'),
        )

    creater_id = models.ForeignKey("User", related_name="user", db_column="creater_id") # CASCADE 되면 안됨
    category = models.SmallIntegerField('category', choices=Category.category, default=Category.RECYCLE)
    # TODO: reported counts -> likes 처럼 관리하기
    reported_counts = models.SmallIntegerField(default=0)
    difficulty = models.SmallIntegerField('difficulty', choices=Difficulty.difficulty, default=Difficulty.EASY)
    logo_img_url = models.CharField(max_length=200)
    icon_img_url = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)