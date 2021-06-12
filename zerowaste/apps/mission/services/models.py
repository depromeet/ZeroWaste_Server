from apps.mission.models.mission import Mission
from apps.mission.models.participation import Participation
from apps.mission.models.likes import MissionLike, CertificationLike
from apps.mission.models.certification import Certification

import pytz
from datetime import datetime
from django.utils import timezone

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
    now_date = timezone.now()
    end_date = now_date + timezone.timedelta(days=_UNIT_DAY_BY_DIFFICULTY[difficulty])
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


def create_certification(certification_data, owner, mission_id, public_url_list):
    certification = Certification(mission_id=get_mission_by_id(mission_id),
                                  owner=owner,
                                  content=certification_data.get('content', ''),
                                  img_urls=public_url_list,
                                  percieved_difficulty=certification_data['percieved_difficulty'])
    certification.save()
    return certification

def get_certification_by_id(certification_id):
    certification = Certification.objects.get(id=certification_id)
    return certification

def get_certification_by_mission_id(mission_id):
    certification = Certification.objects.filter(mission_id=mission_id)
    return certification

def get_certification_by_mission_and_id(mission_id, id):
    certification = Certification.objects.get(mission_id=mission_id, id=id)
    return certification

def get_certifications_by_mission_id_and_owner(mission_id, owner):
    try:
        certification = Certification.objects.filter(mission_id=mission_id, owner=owner)
        return certification
    except Certification.DoesNotExist:
        return None

def update_participation_by_certification(owner, mission_id):
    try:
        participation = get_participation_by_mission_and_owner(owner=owner, mission=mission_id)
        participation.status = Participation.Status.SUCCESS
        participation.save()
        return participation
    except AttributeError:
        return None

def check_overlimit_certifications(owner, mission_id):
    try:
        participation = Participation.objects.get(owner=owner, mission=mission_id, status=Participation.Status.SUCCESS)
        if participation is True:
            return False
    except Participation.DoesNotExist:
        return None

def check_mission_due_date(now_date, mission_id, owner):
    kst = pytz.timezone('Asia/Seoul')
    participation = get_participation_by_mission_and_owner(mission_id, owner)
    due_date = participation.end_date
    if now_date.replace(tzinfo=kst) > due_date.replace(tzinfo=kst):
        participation.status = Participation.Status.FAILURE
        participation.save()


# TODO : 랭킹 기준으로 TOP 3
# def get_top3_ranker_user(owner, mission_id):
#     return


def get_liked_missions_counts_by_missions(mission):
    result = MissionLike.objects.filter(mission=mission).count()
    return result


def get_participations_after_end_date(status=Participation.Status.READY, is_cron_checked=False):
    now = datetime.now()
    participations = Participation.objects.filter(end_date__lt=now, is_cron_checked=is_cron_checked)
    return participations
