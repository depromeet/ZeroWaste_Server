from rest_framework import viewsets, mixins, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator

from apps.user.models.bazzi import Bazzi
from apps.user.serializers.models import BazziSerializer
from apps.core import constants

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='create',
    decorator=swagger_auto_schema(
        # tags=['bazzi'],
        operation_description="Bazzi 생성 \n 이 기능은 어드민 유저만 가능합니다.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: BazziSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='partial_update',
    decorator=swagger_auto_schema(
        # tags=['missions'],
        operation_description="Bazzi 정보 업데이트(부분) \n 이 기능은 어드민 유저만 가능합니다.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: BazziSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='update',
    decorator=swagger_auto_schema(
        # tags=['missions'],
        operation_description="Bazzi 정보 업데이트(덮어쓰기) \n 이 기능은 어드민 유저만 가능합니다.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: BazziSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='destroy',
    decorator=swagger_auto_schema(
        # tags=['missions'],
        operation_description="Bazzi 정보 삭제 \n 이 기능은 어드민 유저만 가능합니다.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: BazziSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
class BazziViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    permission_classes_by_action = {'list': [permissions.AllowAny], 'retrieve': [permissions.AllowAny]}
    queryset = Bazzi.objects
    serializer_class = BazziSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        return super(BazziViewSet, self).get_permissions()
