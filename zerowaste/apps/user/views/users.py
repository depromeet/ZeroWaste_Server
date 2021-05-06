from rest_framework import viewsets, mixins, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from apps.user.serializers.models import UserSerializer
from apps.core import permissions as custom_permission
from apps.core import constants, exceptions
from apps.core.utils.response import build_response_body
from apps.user.services.users import nickname_double_check

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='partial_update',
    decorator=swagger_auto_schema(
        tags=['users'],
        operation_description="User 정보 업데이트(부분)",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: UserSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='update',
    decorator=swagger_auto_schema(
        tags=['users'],
        operation_description="User 정보 전체 업데이트(덮어쓰기)",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: UserSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
@method_decorator(name='destroy',
    decorator=swagger_auto_schema(
        tags=['users'],
        operation_description="User 정보 삭제",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description=constants.USER_JWT_TOKEN
            ),
        ],
        responses={
            200: UserSerializer,
            401: 'Authentication Failed(40100)',
            403: 'Permission denied(403)',
            404: 'Not found(404)'
        }
    )
)
class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [custom_permission.IsOwnerOrReadOnly]
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def partial_update(self, request, *args, **kwargs):
        nickname_double_check(request.user, request.data.get('nickname', None))
        return super().partial_update(request, *args, **kwargs, partial=True)


@swagger_auto_schema(
    method='get',
    tags=['users'],
    operation_description="중복확인 테스트",
    manual_parameters=[openapi.Parameter(
        'nickname',
        openapi.IN_QUERY,
        description='닉네임 중복확인용 API ',
        type=openapi.TYPE_STRING,
        default=None
    ),
     openapi.Parameter(
         'Authorization', openapi.IN_HEADER,
         type=openapi.TYPE_STRING,
         description=constants.USER_JWT_TOKEN
     )])
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
def double_check(request):
    nickname = request.GET.get("nickname", None)
    if not nickname:
        raise exceptions.ValidationError("no nickname parameter")

    nickname_double_check(request.user, nickname)
    return Response(data=build_response_body(data={'state': 'available'}), status=status.HTTP_200_OK)