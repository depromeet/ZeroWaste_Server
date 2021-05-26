from rest_framework import viewsets, mixins, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils.decorators import method_decorator

from apps.core import permissions as custom_permission
from apps.user.serializers.models import ReportedUserSerializer
from apps.user.models.reported_user import ReportedUser
from apps.core import constants

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@method_decorator(name='create',
                  decorator=swagger_auto_schema(
                      tags=['reported_user'],
                      operation_description="신고된 유저 기록 생성",
                      manual_parameters=[
                          openapi.Parameter(
                              'Authorization', openapi.IN_HEADER,
                              type=openapi.TYPE_STRING,
                              description=constants.USER_JWT_TOKEN
                          ),
                      ],
                      responses={
                          200: ReportedUserSerializer,
                          401: 'Authentication Failed(40100)',
                          403: 'Permission denied(403)',
                          404: 'Not found(404)'
                      }
                  )
                )

@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(
                      tags=['reported_user'],
                      operation_description="신고된 유저 정보 업데이트",
                      manual_parameters=[
                          openapi.Parameter(
                              'Authorization', openapi.IN_HEADER,
                              type=openapi.TYPE_STRING,
                              description=constants.USER_JWT_TOKEN
                          ),
                      ],
                      responses={
                          200: ReportedUserSerializer,
                          401: 'Authentication Failed(40100)',
                          403: 'Permission denied(403)',
                          404: 'Not found(404)'
                      }
                  ))

class ReportedUserViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [custom_permission.IsOwnerOrReadOnly]
    permission_classes_by_action = {'create' : [permissions.AllowAny]}
    queryset = ReportedUser.objects
    serializer_class = ReportedUserSerializer