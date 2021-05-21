from django.urls import path, include
from apps.mission.views import missions, certification, participations, likes, scraps
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('missions', missions.MissionViewSet)
router.register('certification', certification.CertificationViewSet)
router.register('^missions/(?P<mission_id>[0-9]+)/participations', participations.ParticipationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('missions/<int:mission_id>/like', likes.MissionLikeViewSet.as_view({'post': 'create'})),
    path('missions/<int:mission_id>/dislike', likes.MissionLikeViewSet.as_view({'delete': 'destroy'})),
    path('missions/<int:mission_id>/scrap', scraps.MissionScrapViewSet.as_view({'post': 'create'})),
    path('missions/<int:mission_id>/unscrap',
         scraps.MissionScrapViewSet.as_view({'delete': 'destroy'})),
]
