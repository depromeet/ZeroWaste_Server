from django.urls import path, include
from apps.mission.views import missions
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('missions', missions.MissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
