from rest_framework import status, permissions, views
from rest_framework.response import Response

from apps.user.serializers import social_login, models
from apps.core import exceptions
from apps.core.utils.response import build_response_body
from apps.user.services import kakao_account
from apps.user.models.auth import Auth
from apps.user.services.models import create_anonymous_user, get_auth_by_identifier_with_login_type, create_auth, record_user_token

from drf_yasg.utils import swagger_auto_schema
import logging


class KakaoLoginAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="카카오 로그인 시 토큰 등록 및 익명 유저생성",
        request_body=social_login.KakaoLoginSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = social_login.KakaoLoginSerializer(data=request.data)
        if serializer.is_valid():
            kakao_access_token = serializer.validated_data['kakao_access_token']
            logging.debug(f'kakao access token : {kakao_access_token}')
            kakao_user_profile = kakao_account.get_user_profile(kakao_access_token)
            print("kakao user profile for : ", kakao_user_profile)

            logging.debug(f"kakao user profile for : {kakao_user_profile}")
            kakao_user_id = kakao_user_profile['id']
            try:
                is_new_user = False
                auth = get_auth_by_identifier_with_login_type(identifier=str(kakao_user_id), login_type=Auth.LoginType.Kakao)

            except Auth.DoesNotExist:
                anonymous_user = create_anonymous_user()
                auth = create_auth(identifier=kakao_user_id, email=None, user=anonymous_user, social_token=kakao_access_token, login_type=Auth.LoginType.Kakao)
                is_new_user = True

            auth = record_user_token(auth)
            auth_serializer = models.AuthSerializer(auth)
            result = auth_serializer.data
            result['is_new_user'] = is_new_user
            return Response(build_response_body(result), status=status.HTTP_200_OK)
        raise exceptions.ValidationError()


class AppleLoginAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="애플 로그인 시 토큰 등록 및 익명 유저생성",
        request_body=social_login.AppleLoginSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = social_login.AppleLoginSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['identifier']
            email = serializer.validated_data.get('email', None)
            logging.debug(f'apple identifier : {identifier}')

            try:
                is_new_user = False
                auth = get_auth_by_identifier_with_login_type(identifier=identifier, login_type=Auth.LoginType.Apple)

            except Auth.DoesNotExist:
                anonymous_user = create_anonymous_user()
                auth = create_auth(identifier=identifier, email=email, user=anonymous_user, social_token=identifier, login_type=Auth.LoginType.Apple)
                is_new_user = True

            auth = record_user_token(auth)
            auth_serializer = models.AuthSerializer(auth)
            result = auth_serializer.data
            result['is_new_user'] = is_new_user
            return Response(build_response_body(result), status=status.HTTP_200_OK)
        raise exceptions.ValidationError()