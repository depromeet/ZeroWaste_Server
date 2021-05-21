from django.db import models


class MissionScrap(models.Model):
    id = models.BigAutoField(primary_key=True)
    mission = models.ForeignKey("Mission", related_name="scrapped_mission", on_delete=models.CASCADE,
                                   db_column="mission_id")
    owner = models.ForeignKey("user.User", related_name="mission_scrapper", on_delete=models.CASCADE,
                                db_column="owner")
