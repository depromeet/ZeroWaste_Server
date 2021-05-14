from rest_framework import serializers

from apps.mission.models.mission import Mission
from apps.mission.models.certification import Certification
from apps.core.utils.response import build_response_body
from apps.user.services.models import get_user_by_id
from apps.user.serializers.models import UserSerializer


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ('id', 'name', 'owner', 'category', "difficulty", "logo_img_url", "icon_img_url", "content")

    def validate(self, attrs):
        return self.initial_data

    def to_internal_value(self, data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            self.initial_data['owner'] = user

    #TODO: 해당 사용자가 인증을 작성할 수 있는지 여부 -> can_write_certification : Participation 객체 여부
    def to_representation(self, instance):
        value = super(MissionSerializer, self).to_representation(instance)
        creater = get_user_by_id(value['owner'])
        value['creater'] = UserSerializer(creater).data['data']
        return build_response_body(data=value)


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ('id', 'name', 'owner', 'mission_id', "image", "content", 'isPublic')

    def validate(self, attrs):
        return self.initial_data

    def to_internal_value(self, data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            self.initial_data['owner'] = user

    #TODO: ?? certification에서는 creater 로 키를 바꾸기보다, 그냥 owner 정보로 보여져도 될거같은데요?
    def to_representation(self, instance):
        value = super(CertificationSerializer, self).to_representation(instance)
        creater = get_user_by_id(value['owner'])
        value['creater'] = UserSerializer(creater).data['data']
        return build_response_body(data=value)