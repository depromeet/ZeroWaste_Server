from django.db import models
from django.utils import timezone

from apps.core.models.model_base import ModelBase
from apps.core import exceptions


class SoftDeleteModelBase(ModelBase):
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        if self.deleted_at:
            raise exceptions.SoftDeleteError(
                detail=f'table:{self.__class__.__name__} id:{self.id} is already deleted'
            )
        self.deleted = timezone.now()
        self.save()

    def undelete(self, *args, **kwargs):
        if not self.deleted:
            raise exceptions.SoftDeleteError(
                detail=f'table:{self.__class__.__name__} id:{self.id} is not deleted'
            )
        self.deleted = None
        self.save()
