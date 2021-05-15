from rest_framework import serializers

from apps.mission.models.mission import Mission
from apps.mission.models.certification import Certification
from apps.mission.models.participation import Participation
from apps.core.utils.response import build_response_body
from apps.user.services.models import get_user_by_id
from apps.user.serializers.models import UserSerializer
from apps.core.exceptions import ValidationError


class MissionSerializer(serializers.ModelSerializer):
    _THEME_LIST = ('refuse', 'reduce', 'reuse', 'recycle', 'rot')

    class Meta:
        model = Mission
        fields = ('id', 'name', 'owner', 'place', 'theme', "difficulty", "logo_img_url", "icon_img_url", "content")

    def validate(self, data):
        if not self.initial_data['place'] in Mission.Place:
            raise ValidationError(f'place is not in {Mission.Place.choices}')

        if not self.initial_data['difficulty'] in Mission.Difficulty:
            raise ValidationError(f'difficulty is not in {Mission.Difficulty.choices}')

        for theme_item in self.initial_data['theme']:
            if not theme_item in self._THEME_LIST:
                raise ValidationError(f'{theme_item} is not in {self._THEME_LIST}')

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
        value['theme'] = instance.theme
        return build_response_body(data=value)


class ParticipationSerializer(serializers.ModelSerializer):
    mission_id = MissionSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = ('id', 'mission_id', 'owner', 'status', 'start_date', 'end_date')


class CertificationSerializer(serializers.ModelSerializer):
    mission_id = ParticipationSerializer(read_only=True)

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

    # TODO: ?? certification에서는 creater로 키를 바꾸기보다, 그냥 owner 정보로 보여져도 될거같은데요?
    def to_representation(self, instance):
        value = super(CertificationSerializer, self).to_representation(instance)
        creater = get_user_by_id(value['owner'])
        value['creater'] = UserSerializer(creater).data['data']
        return build_response_body(data=value)
