from rest_framework import viewsets, mixins, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator

from apps.core import permissions as custom_permission
from apps.mission.serializers.models import ParticipationSerializer
from apps.mission.models.participation import Participation
from apps.mission.models.mission import Mission
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.core import constants
from datetime import datetime

class ParticipationViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Participation.objects
    serializer_class = ParticipationSerializer

    def create(self, request, *args, **kwargs):
        mission_id = request.data['mission_id']
        mission = Mission.objects.get(id=mission_id)
        if mission.level == Mission.Difficulty.EASY:
            unit_day = 3
            now = datetime.now()
            Participation.objects.create(start_date = now, end_date = now+unit_day)