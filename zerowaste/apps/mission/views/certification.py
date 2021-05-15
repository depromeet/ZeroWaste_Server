from rest_framework import viewsets, mixins, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator

from apps.core import permissions as custom_permission
from apps.mission.serializers.models import CertificationSerializer
from apps.mission.models.certification import Certification

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.core import constants


@method_decorator(name='create',
    decorator=swagger_auto_schema(
        tags=['certification'],
        operation_description="새로운 인증 정보 생성",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: CertificationSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='partial_update',
    decorator=swagger_auto_schema(
        tags=['certification'],
        operation_description="인증 정보 업데이트(부분)",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: CertificationSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='update',
    decorator=swagger_auto_schema(
        tags=['certification'],
        operation_description="인증 정보 전체 업데이트(덮어쓰기)",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: CertificationSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='destroy',
    decorator=swagger_auto_schema(
        tags=['certification'],
        operation_description="인증 정보 삭제",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: CertificationSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
class CertificationViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [custom_permission.IsOwnerOrReadOnly]
    permission_classes_by_action = {'create': [permissions.AllowAny]}
    queryset = Certification.objects
    serializer_class = CertificationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [custom_permission.IsOwnerOrReadOnly]
        return super(CertificationViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        #TODO: participation 객체 생성 여부 체크
        return super(CertificationViewSet, self).create(request, *args, **kwargs)