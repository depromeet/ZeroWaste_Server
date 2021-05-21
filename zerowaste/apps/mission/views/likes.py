from rest_framework import views, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.utils.response import build_response_body
from apps.mission.models.likes import MissionLike
from apps.mission.services.models import get_mission_by_id
from apps.core import constants


@method_decorator(name='create',
    decorator=swagger_auto_schema(
        tags=['missions'],
        opertion_description="Mission 좋아요 등록",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: '{"state": "object created"}}',
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='destroy',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 좋아요 등록",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: '{"state": "object deleted"}}',
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
class MissionLikeAPIView(viewsets.GenericViewSet):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, mission_id):
        MissionLike.objects.get_or_create(
            mission=get_mission_by_id(mission_id),
            owner=self.request.user
        )
        return Response(data=build_response_body({'state': 'object created'}), status=status.HTTP_200_OK)

    def destroy(self, request, mission_id):
        MissionLike.objects.filter(
            mission=get_mission_by_id(mission_id),
            owner=self.request.user
        ).delete()
        return Response(data=build_response_body({'state': 'object deleted'}), status=status.HTTP_200_OK)
