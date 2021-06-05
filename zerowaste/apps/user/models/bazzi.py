from apps.core.models.soft_delete_model_base import ModelBase
from django.db import models


class Bazzi(ModelBase):
    name = models.CharField(max_length=20)
    icon_url = models.URLField()
    description = models.CharField(max_length=100, help_text="bazzi를 받게되는 이벤트 설명")


class User_Bazzi(models.Model):
    id = models.BigAutoField(primary_key=True)
    bazzi = models.ForeignKey("Bazzi", related_name="own_bazzi", on_delete=models.CASCADE,
                              db_column="bazzi")
    owner = models.ForeignKey("User", related_name="bazzi_owner", on_delete=models.CASCADE,
                              db_column="owner")
