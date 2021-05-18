from rest_framework import serializers

from apps.user.models.auth import Auth
from apps.user.models.user import User
from apps.user.models.blacklist import BlackList
from apps.mission.models.participation import Participation
from apps.core.utils.response import build_response_body
from apps.mission.services.models import get_participations_by_owner


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ('id', 'identifier', 'email', 'created_at', "token", "user_id")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'level', 'is_notify', 'description')

    def to_representation(self, instance):
        value = super(UserSerializer, self).to_representation(instance)
        value['completed_mission_counts'] = len(get_participations_by_owner(instance))
        value['progressing_mission_counts'] = len(get_participations_by_owner(instance, status=Participation.Status.READY))
        return build_response_body(data=value)


class BlackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlackList
        fields = ('id', 'target_user_id', 'reporter_id', 'description')