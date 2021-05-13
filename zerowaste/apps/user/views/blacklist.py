from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from apps.core import permissions as custom_permission
from apps.user.serializers.models import BlackListSerializer
from apps.user.models import blacklist

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class BlackListViewSet(viewsets.GenericViewSet,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin):
    permission_classes = [custom_permission.IsOwnerOrReadOnly]
    queryset = get_user_model().objects
    serializer_class = BlackListSerializer