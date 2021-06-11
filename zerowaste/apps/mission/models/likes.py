from django.db import models


class MissionLike(models.Model):
    id = models.BigAutoField(primary_key=True)
    mission = models.ForeignKey("Mission", related_name="like_mission", on_delete=models.CASCADE,
                                   db_column="mission_id")
    owner = models.ForeignKey("user.User", related_name="mission_like_user", on_delete=models.CASCADE,
                                db_column="owner")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.mission.update_likes_count()


class CertificationLike(models.Model):
    id = models.BigAutoField(primary_key=True)
    certification_id = models.ForeignKey("Mission", related_name="certification_like_mission",
                                         on_delete=models.DO_NOTHING,
                                         db_column="certification_id")
    owner = models.ForeignKey("user.User", related_name="certification_like_user", on_delete=models.CASCADE,
                                db_column="owner")