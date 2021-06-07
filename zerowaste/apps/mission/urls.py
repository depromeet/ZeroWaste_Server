from django.urls import path, include
from apps.mission.views import missions, certifications, participations, likes
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('missions', missions.MissionViewSet)
router.register('^missions/(?P<mission_id>[0-9]+)/certifications', certifications.CertificationViewSet)
router.register('^missions/(?P<mission_id>[0-9]+)/participations', participations.ParticipationViewSet)
# TODO: Ranking view => mission_id만 있으면 될 듯

urlpatterns = [
    path('', include(router.urls)),
    path('missions/<int:mission_id>/like', likes.MissionLikeViewSet.as_view({'post': 'create'})),
    path('missions/<int:mission_id>/dislike', likes.MissionLikeViewSet.as_view({'delete': 'destroy'})),
    path('batch/participations', missions.update_participation_status)
]
