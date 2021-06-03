from rest_framework import serializers

from apps.mission.models.mission import Mission
from apps.mission.models.certification import Certification
from apps.mission.models.participation import Participation
from apps.mission.models.likes import MissionLike
from apps.mission.services.models import get_participation_by_mission_and_owner, \
    is_user_liked_mission, get_number_of_participation_by_mission, get_liked_missions_counts_by_missions
from apps.core.utils.response import build_response_body
from apps.user.services.models import get_user_by_id
from apps.user.serializers.models import UserSerializer
from apps.core.exceptions import ValidationError


class MissionSerializer(serializers.ModelSerializer):
    signed_url_num = serializers.IntegerField(required=False)
    _THEME_LIST = ('refuse', 'reduce', 'reuse', 'recycle', 'rot')

    class Meta:
        model = Mission
        fields = (
        'id', 'name', 'owner', 'place', 'theme', "difficulty", "banner_img_urls", "content",
        'sentence_for_cheer', 'signed_url_num')

    def validate(self, data):
        place = self.initial_data.get('place', None)
        if place and not place in Mission.Place:
            raise ValidationError(f'{self.initial_data["place"]} is not in {Mission.Place.choices}')

        difficulty = self.initial_data.get('difficulty', None)
        if difficulty and not difficulty in Mission.Difficulty:
            raise ValidationError(
                f'{self.initial_data["difficulty"]} is not in {Mission.Difficulty.choices}')

        theme = self.initial_data.get('theme', [])
        for theme_item in theme:
            if not theme_item in self._THEME_LIST:
                raise ValidationError(f'{theme_item} is not in {self._THEME_LIST}')

        return self.initial_data

    def to_internal_value(self, data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            self.initial_data['owner'] = request.user

    def to_representation(self, instance):
        value = super(MissionSerializer, self).to_representation(instance)
        creater = get_user_by_id(value['owner'])
        value['creater'] = UserSerializer(creater).data['data']
        value['theme'] = instance.theme
        value['banner_img_urls'] = instance.banner_img_urls

        request = self.context.get("request")
        if request and not request.user.is_anonymous:
            participation = get_participation_by_mission_and_owner(instance, request.user)
            if participation:
                value['participation'] = ParticipationSerializer(participation).data
            else:
                value['participation'] = {'status': 'none'}
            value['is_liked'] = is_user_liked_mission(instance, request.user)

        if request:
            pk = request.parser_context['kwargs'].get('pk', None)
            if not pk: # (hasattr(self, 'action') and self.action == 'list')
                return value
        return build_response_body(data=value)


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ('id', 'status', 'start_date', 'end_date')

    def to_internal_value(self, data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            self.initial_data['owner'] = request.user


class ParticipationNoneFieldSerializer(serializers.BaseSerializer):
    class Meta:
        model = Participation
        fields = ''


class MissionLikeSerializer(serializers.BaseSerializer):
    class Meta:
        model = MissionLike
        fields = ''


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
            self.initial_data['owner'] = request.user

    # TODO: ?? certification에서는 creater로 키를 바꾸기보다, 그냥 owner 정보로 보여져도 될거같은데요?
    def to_representation(self, instance):
        value = super(CertificationSerializer, self).to_representation(instance)
        creater = get_user_by_id(value['owner'])
        value['creater'] = UserSerializer(creater).data['data']
        return build_response_body(data=value)
