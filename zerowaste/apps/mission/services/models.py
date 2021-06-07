from apps.mission.models.mission import Mission
from apps.mission.models.participation import Participation
from apps.mission.models.likes import MissionLike

from datetime import timedelta
from django.utils.timezone import now

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


def create_mission(mission_data, owner, public_url_list):
    mission = Mission(name=mission_data['name'], owner=owner, place=mission_data['place'],
                      theme=mission_data['theme'], difficulty=mission_data['difficulty'],
                      banner_img_urls=public_url_list, content=mission_data.get('content', ''), sentence_for_cheer=mission_data.get('sentence_for_cheer', ""))
    mission.save()
    return mission


def get_participation_by_mission_and_owner(mission, owner):
    try:
        participation = Participation.objects.get(mission=mission, owner=owner)
        return participation
    except Participation.DoesNotExist:
        return None


def get_participation_period(difficulty):
    now_date = now
    end_date = now_date + timedelta(days=_UNIT_DAY_BY_DIFFICULTY[difficulty])
    return now_date, end_date


def create_participation(mission, owner):
    participation = get_participation_by_mission_and_owner(mission, owner)
    if not participation:
        now_date, end_date = get_participation_period(mission.difficulty)
        participation = Participation(mission=mission, owner=owner, start_date=now_date,
                                      end_date=end_date)
        participation.save()
    return participation


def get_participation_by_id(participation_id):
    participation = Participation.objects.get(id=participation_id)
    return participation


def update_participation_status(participation_id, mission, status):
    participation = get_participation_by_id(participation_id)
    participation.status = status
    now_date, end_date = get_participation_period(mission.difficulty)
    participation.start_date = now_date
    participation.end_date = end_date
    participation.save()
    return participation


def get_participations_by_owner(owner, status=Participation.Status.SUCCESS):
    participations = Participation.objects.filter(owner=owner, status=status)
    return participations


def get_number_of_participation_by_mission(mission, status=Participation.Status.SUCCESS):
    participations = Participation.objects.filter(mission=mission, status=status)
    return participations


def is_user_liked_mission(mission, user):
    result = True if MissionLike.objects.filter(mission=mission, owner=user) else False
    return result


def get_liked_missions_by_owner(owner):
    liked_missions = MissionLike.objects.filter(owner=owner)
    return liked_missions


def get_liked_missions_counts_by_missions(mission):
    result = MissionLike.objects.filter(mission=mission).count()
    return result


def get_participations_after_end_date(status=Participation.Status.READY, is_cron_checked=False):
    now = datetime.now()
    participations = Participation.objects.filter(end_date__lt=now, is_cron_checked=is_cron_checked)
    return participations
