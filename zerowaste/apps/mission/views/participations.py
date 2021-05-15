from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.mission.serializers.models import ParticipationSerializer
from apps.mission.models.participation import Participation
from apps.core import constants
from apps.core.mixins import PartialUpdateModelMixin
from apps.core.utils.response import build_response_body
from apps.core.utils.tools import to_dict
from apps.mission.services import models


@method_decorator(name='create',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 수락 시 객체 생성",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: ParticipationSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='partial_update',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 재시도 시 객체 업데이트",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: ParticipationSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
class ParticipationViewSet(viewsets.GenericViewSet):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Participation.objects

    def create(self, request, mission_id):
        participation = models.create_participation(models.get_mission_by_id(mission_id), request.user)
        return Response(build_response_body(data=to_dict(participation)), status=status.HTTP_200_OK)

    def partial_update(self, request, mission_id, pk):
        participation = models.update_participation_status(pk, models.get_mission_by_id(mission_id), Participation.Status.READY)
        return Response(build_response_body(data=to_dict(participation)), status=status.HTTP_200_OK)
