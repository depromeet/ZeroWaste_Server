from apps.core.models.soft_delete_model_base import SoftDeleteModelBase
from django.db import models


class BlockList(SoftDeleteModelBase):
    class Description:
        SEXUAL = 0
        VIOLENCE = 1
        HATE = 2
        SPAM = 3
        ILLEGAL = 4
        description = (
            (SEXUAL, 'sexual'),
            (VIOLENCE, 'violence'),
            (HATE, 'hate'),
            (SPAM, 'spam'),
            (ILLEGAL, 'illegal')
        )

    target_user_id = models.ForeignKey("user.User", related_name="target_user", on_delete=models.DO_NOTHING,
                                       db_column="target_user_id")
    reporter_id = models.ForeignKey("user.User", related_name="reported_user", on_delete=models.DO_NOTHING,
                                       db_column="reporter_id")
    description = models.SmallIntegerField('description', choices=Description.description, default=Description.SPAM)