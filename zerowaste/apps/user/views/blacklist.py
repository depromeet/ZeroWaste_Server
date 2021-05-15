from rest_framework import viewsets, mixins, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator

from apps.core import permissions as custom_permission
from apps.user.serializers.models import BlackListSerializer
from apps.user.models.blacklist import BlackList
from apps.core import constants

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      tags=['blacklist'],
                      operation_description="blacklist 기록 생성",
                      manual_parameters=[
                          openapi.Parameter(
                              'Authorization', openapi.IN_HEADER,
                              type=openapi.TYPE_STRING,
                              description=constants.USER_JWT_TOKEN
                          ),
                      ],
                      responses={
                          200: BlackListSerializer,
                          401: 'Authentication Failed(40100)',
                          403: 'Permission denied(403)',
                          404: 'Not found(404)'
                      }
                  )
                )

@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(
                      tags=['blacklist'],
                      operation_description="Blacklist 정보 업데이트",
                      manual_parameters=[
                          openapi.Parameter(
                              'Authorization', openapi.IN_HEADER,
                              type=openapi.TYPE_STRING,
                              description=constants.USER_JWT_TOKEN
                          ),
                      ],
                      responses={
                          200: BlackListSerializer,
                          401: 'Authentication Failed(40100)',
                          403: 'Permission denied(403)',
                          404: 'Not found(404)'
                      }
                  ))

class BlackListViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [custom_permission.IsOwnerOrReadOnly]
    permission_classes_by_action = {'create' : [permissions.AllowAny]}
    queryset = BlackList.objects
    serializer_class = BlackListSerializer