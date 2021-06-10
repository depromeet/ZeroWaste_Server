from django.contrib import admin

from apps.mission.models.mission import Mission
from apps.mission.models.certification import Certification
from apps.mission.models.likes import MissionLike, CertificationLike


admin.site.register(Mission)
admin.site.register(MissionLike)
admin.site.register(Certification)
admin.site.register(CertificationLike)