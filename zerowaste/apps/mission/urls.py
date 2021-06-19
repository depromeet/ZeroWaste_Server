from django.urls import path, include
from apps.mission.views import missions, certifications, participations, likes
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('missions', missions.MissionViewSet)
router.register('^missions/(?P<mission_id>[0-9]+)/certifications', certifications.CertificationViewSet)
router.register('certifications', certifications.GetCertificationInfoViewset)
router.register('certifications/liked',certifications.LikedCertificationByUserViewset)
router.register('certifications/created', certifications.CreatedCertificationByUserViewset)
router.register('^missions/(?P<mission_id>[0-9]+)/participations', participations.ParticipationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('missions/<int:mission_id>/like', likes.MissionLikeViewSet.as_view({'post': 'create'})),
    path('missions/<int:mission_id>/dislike', likes.MissionLikeViewSet.as_view({'delete': 'destroy'})),
    path('batch/participations', missions.update_participation_status),
    path('certifications/<int:certification_id>/like', likes.CertificationLikeViewSet.as_view({'post': 'create'})),
    path('certifications/<int:certification_id>/dislike', likes.CertificationLikeViewSet.as_view({'delete': 'destroy'}))
]