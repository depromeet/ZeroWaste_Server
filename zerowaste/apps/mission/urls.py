from django.urls import path, include
from apps.mission.views import missions, certification
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('missions', missions.MissionViewSet)
router.register('certification', certification.CertificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
