from django.contrib import admin

from apps.mission.models.mission import Mission, MissionLiker
from apps.mission.models.certification import Certification, CertificationLiker


admin.site.register(Mission)
admin.site.register(MissionLiker)
admin.site.register(Certification)
admin.site.register(CertificationLiker)