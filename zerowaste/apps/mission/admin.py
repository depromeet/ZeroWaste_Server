from django.contrib import admin

# Register your models here.

from apps.mission.models.mission import Mission, Mission_liker

admin.site.register(Mission)
admin.site.register(Mission_liker)