from rest_framework import serializers
from apps.user.models.auth import Auth


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ('id', 'identifier', 'email', 'created_at', "token", "user_id")
