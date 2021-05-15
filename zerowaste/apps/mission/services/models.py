from apps.mission.models.mission import Mission
from apps.mission.models.participation import Participation

from datetime import datetime, timedelta

_UNIT_DAY_BY_DIFFICULTY = {
    'very_easy': 1,
    'easy': 3,
    'medium': 5,
    'hard': 7,
    'extra_hard': 14
}


def get_mission_by_id(mission_id):
    mission = Mission.objects.get(id=mission_id)
    return mission


def get_participation_by_mission_and_owner(mission, owner):
    try:
        #TODO: mission_id -> mission 변경
        participation = Participation.objects.get(mission_id=mission, owner=owner)
        return participation
    except Participation.DoesNotExist:
        return None


def create_participation(mission, owner):
    participation = get_participation_by_mission_and_owner(mission, owner)
    if not participation:
        now_date = datetime.now()
        end_date = now_date + timedelta(days=_UNIT_DAY_BY_DIFFICULTY[mission.difficulty])
        # TODO: mission_id -> mission으로 변경
        participation = Participation(mission_id=mission, owner=owner, start_date=now_date,
                                      end_date=end_date)
        participation.save()
    return participation
