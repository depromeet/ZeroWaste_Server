from rest_framework import status, permissions, views
from rest_framework.response import Response

from apps.user.serializers import social_login, models
from apps.core import exceptions
from apps.user.services import kakao_account
from apps.user.models.auth import Auth
from apps.user.services.models import create_anonymous_user, get_auth_by_identifier_with_login_type, create_auth


class KakaoLoginAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    # @swagger_auto_schema(
    #     operation_description="",
    #     request_body=social_login.KakaoLoginSerializer,
    # )
    def post(self, request, *args, **kwargs):
        serializer = social_login.KakaoLoginSerializer(data=request.data)
        if serializer.is_valid():
            kakao_access_token = serializer.validated_data['kakao_access_token']
            kakao_user_profile = kakao_account.get_user_profile(kakao_access_token)
            kakao_user_id = kakao_user_profile['id']
            try:
                auth = get_auth_by_identifier_with_login_type(identifier=str(kakao_user_id), login_type=Auth.LoginType.Kakao)

            except Auth.DoesNotExist:
                anonymous_user = create_anonymous_user()
                auth = create_auth(identifier=kakao_user_id, email=None, user=anonymous_user, social_token=kakao_access_token, login_type=Auth.LoginType.Kakao)

            auth_serializer = models.AuthSerializer(auth)
            return Response(auth_serializer.data, status=status.HTTP_200_OK)
        raise exceptions.ValidationError()
