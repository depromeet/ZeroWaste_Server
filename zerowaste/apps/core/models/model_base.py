from django.db import models


class ModelBase(models.Model):
    id = models.BigAutoField(primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"id: {self.id} created:{self.created_at} updated:{self.updated_at} deleted: {self.deleted_at}"