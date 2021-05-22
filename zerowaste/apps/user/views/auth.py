from rest_framework_jwt import views as jwt_views
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status, permissions, views
from rest_framework.response import Response

from apps.user.services.models import get_auth_by_user_id, record_user_token
from apps.user.serializers import models
from apps.core.utils.response import build_response_body
from apps.core.exceptions import InternalServerError


class CustomRefreshJSONWebToken(jwt_views.RefreshJSONWebToken):
    serializer_class = jwt_views.RefreshJSONWebTokenSerializer
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            response = super(CustomRefreshJSONWebToken, self).post(request, *args, **kwargs)

            auth = get_auth_by_user_id(user.id)
            auth = record_user_token(auth, response.data['token'])
            auth_serializer = models.AuthSerializer(auth)
            return Response(build_response_body(auth_serializer.data), status=status.HTTP_200_OK)
        raise InternalServerError()