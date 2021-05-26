from apps.core.models.model_base import ModelBase
from django.db import models

class BlockList(ModelBase):
    class Description(models.TextChoices):
        SEXUAL = 'sexual'
        VIOLENCE = 'violence'
        HATE = 'hate'
        SPAM = 'spam'
        ILLEGAL = 'illegal'

    target_user_id = models.ForeignKey("user.User", related_name="target_user", on_delete=models.DO_NOTHING,
                                       db_column="target_user_id")
    reporter_id = models.ForeignKey("user.User", related_name="reported_user", on_delete=models.DO_NOTHING,
                                       db_column="reporter_id")
    description = models.SmallIntegerField('description', choices=Description.choices)
