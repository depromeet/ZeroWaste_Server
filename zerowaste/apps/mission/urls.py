from django.urls import path, include
from apps.mission.views import missions, certification, participations
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('missions', missions.MissionViewSet)
router.register('certification', certification.CertificationViewSet)
router.register('^missions/(?P<mission_id>[0-9]+)/participations', participations.ParticipationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
