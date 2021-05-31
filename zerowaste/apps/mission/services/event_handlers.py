from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.mission.models.mission import Mission
from apps.user.models.bazzi import User_Bazzi
from apps.user.services.models import get_bazzi_by_id

_FIRST_MISSION_CREATE_BAZZI_ID = 1


@receiver(post_save, sender=Mission)
def mission_save(sender, instance, **kwargs):
    owner_mission_list = Mission.objects.filter(owner=instance.owner)
    if len(owner_mission_list) == 1:
        first_mission_create_bazzi = get_bazzi_by_id(bazzi_id=_FIRST_MISSION_CREATE_BAZZI_ID)
        User_Bazzi.objects.get_or_create(
            bazzi=first_mission_create_bazzi,
            owner=instance.owner
        )
