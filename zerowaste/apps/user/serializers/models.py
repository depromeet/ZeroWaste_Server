from rest_framework import serializers
from apps.user.models.auth import Auth
from apps.user.models.user import User
from apps.core.utils.response import build_response_body


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ('id', 'identifier', 'email', 'created_at', "token", "user_id")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'level', 'reported_counts', 'is_notify')

    def to_representation(self, instance):
        value = super(UserSerializer, self).to_representation(instance)
        return build_response_body(data=value)