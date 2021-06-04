from rest_framework import viewsets, mixins, permissions, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from apps.core import permissions as custom_permission
from apps.mission.serializers.models import CertificationSerializer
from apps.user.serializers.models import UserSerializer
from apps.mission.services.missions import separate_url_to_signed_public
from apps.mission.services.models import create_certification, get_mission_by_id, update_participation_by_certification, update_participation_status_by_period, get_certifications_by_mission_id
from apps.mission.models.certification import Certification
from apps.core.utils.response import build_response_body
from apps.core.utils.tools import to_dict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.core import constants


@method_decorator(name='list',
    decorator=swagger_auto_schema(
        tags=['certifications'],
        operation_description="미션 인증 목록을 조회합니다.",
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

@method_decorator(name='retrieve',
    decorator=swagger_auto_schema(
        tags=['certifications'],
        operation_description="미션 인증 목록을 조회합니다2.",
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

@method_decorator(name='create',
    decorator=swagger_auto_schema(
        tags=['certifications'],
        operation_description="새로운 미션 인증 정보를 생성합니다.",
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
        tags=['certifications'],
        operation_description="기존의 인증 정보를 업데이트합니다. \n 이미지 삭제 및 수정은 불가능하며, 후기 수정/업데이트만 가능합니다.",
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
        tags=['certifications'],
        operation_description="기존의 인증 정보를 삭제합니다.",
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

    # TODO: certification mission_id에 따라 목록 조회하는 함수 -> mission 조회 함수 swagger로 확인해보기
    def list(self, request, mission_id):
        certification = get_certifications_by_mission_id(mission_id) # keyerror
        return Response(build_response_body(data=to_dict(certification)), status=status.HTTP_200_OK)


    #TODO: participation 객체 생성 여부 체크 및 state -> progress로 업데이트
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            signed_url_num = request.data.get('signed_url_num', 0)
            signed_url_list, public_url_list = separate_url_to_signed_public(signed_url_num, request.user)
            create_certification(serializer.validated_data, request.user, public_url_list)

            update_participation_by_certification(request.user, request.data['mission_id'])
            update_participation_status_by_period(request.user, request.data['mission_id'])

            result = serializer.validated_data
            result['signed_url_list'] = signed_url_list
            # TODO : 단순히 user id만 나오도록 하기
            result['owner'] = UserSerializer(result['owner']).data['data']

            return Response(data=build_response_body(result), status=status.HTTP_200_OK)


    # def partial_update(self, request, mission_id):




# TODO: get_participations_by_owner => completed_mission_counts 변경되도록
# TODO: participation success, failure 등 상태값 변경
