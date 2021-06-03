from rest_framework import viewsets, mixins, permissions, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from apps.core import permissions as custom_permission
from apps.mission.serializers.models import MissionSerializer
from apps.mission.models.mission import Mission
from apps.mission.models.participation import Participation
from apps.mission.services.missions import separate_url_to_signed_public
from apps.mission.services.models import create_mission
from apps.core import constants, exceptions
from apps.core.utils.response import build_response_body
from apps.user.serializers.models import UserSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      tags=['missions'],
                      operation_description="Mission 리스트 조회 \n JWT TOKEN 기입 시 미션 참여 및 좋아요 여부 결과를 받을 수 있습니다.",
                      manual_parameters=[
                          openapi.Parameter(
                              'theme', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description=constants.MISSION_THEME
                          ),
                          openapi.Parameter(
                              'ordering', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description=constants.MISSION_ORDERING
                          ),
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
    filter_fields = ('place', 'difficulty')

    # TODO: v2 theme 중복조회 적용하기
    def get_queryset(self):
        super_queryset = super().get_queryset()
        theme = self.request.query_params.get('theme')
        if theme:
            mission_querysets = super_queryset.filter(theme__contains=theme, is_public=True)
        else:
            mission_querysets = super_queryset.filter(is_public=True)

        ordering = self.request.query_params.get('ordering')
        if ordering == "recent":
            return mission_querysets.order_by('-created_at')
        elif ordering == "popularity":
            return mission_querysets.order_by('-likes_count', '-created_at')
        elif ordering == "participation":
            return mission_querysets.order_by('-successful_count', '-in_progress_count', '-created_at')
        return mission_querysets

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [custom_permission.IsOwnerOrReadOnly]
        return super(MissionViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                signed_url_num = request.data.get('signed_url_num', 0)
                signed_url_list, public_url_list = separate_url_to_signed_public(signed_url_num,
                                                                                 request.user)
                mission = create_mission(serializer.validated_data, request.user, public_url_list)

                result = serializer.validated_data
                result['id'] = int(mission.id)
                result['owner'] = UserSerializer(result['owner']).data['data']
                result['signed_url_list'] = signed_url_list
                return Response(data=build_response_body(result), status=status.HTTP_200_OK)
            except Exception:
                raise exceptions.InternalServerError()

    def list(self, request, *args, **kwargs):
        try:
            response = super(MissionViewSet, self).list(request, *args, **kwargs)
            return Response(data=build_response_body(response.data), status=status.HTTP_200_OK)
        except Exception:
            raise exceptions.InternalServerError()
