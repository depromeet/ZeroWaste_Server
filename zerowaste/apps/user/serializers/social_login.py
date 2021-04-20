from rest_framework import serializers


class KakaoLoginSerializer(serializers.Serializer):
    kakao_access_token = serializers.CharField()
    email = serializers.CharField(required=False)
