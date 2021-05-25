from rest_framework import viewsets, mixins, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend

from apps.core import permissions as custom_permission
from apps.mission.serializers.models import MissionSerializer
from apps.mission.models.mission import Mission
from apps.core import constants

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='list',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 리스트 조회 \n JWT TOKEN 기입 시 미션 참여 및 좋아요 여부 결과를 받을 수 있습니다.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: MissionSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='retrieve',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 객체 조회 \n JWT TOKEN 기입 시 미션 참여 및 좋아요 여부 결과를 받을 수 있습니다.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: MissionSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='create',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 생성",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: MissionSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='partial_update',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 정보 업데이트(부분)",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: MissionSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='update',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 정보 전체 업데이트(덮어쓰기)",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: MissionSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='destroy',
    decorator=swagger_auto_schema(
        tags=['missions'],
        operation_description="Mission 정보 삭제",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: MissionSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
class MissionViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [custom_permission.IsOwnerOrReadOnly]
    permission_classes_by_action = {'create': [permissions.AllowAny]}
    queryset = Mission.objects
    serializer_class = MissionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('place', 'difficulty', 'theme')

    # TODO: v2 theme 중복조회 적용하기
    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [custom_permission.IsOwnerOrReadOnly]
        return super(MissionViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        return super(MissionViewSet, self).create(request, *args, **kwargs)