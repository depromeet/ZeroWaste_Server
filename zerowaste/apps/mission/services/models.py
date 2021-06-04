from apps.mission.models.mission import Mission
from apps.mission.models.participation import Participation
from apps.mission.models.likes import MissionLike
from apps.mission.models.certification import Certification

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
    now_date = datetime.now()
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


def is_user_liked_mission(mission, user):
    result = True if MissionLike.objects.filter(mission=mission, owner=user) else False
    return result


def get_liked_missions_by_owner(owner):
    liked_missions = MissionLike.objects.filter(owner=owner)
    return liked_missions


def create_certification(certification_data, owner, public_url_list):
    certification = Certification(name=certification_data['name'],
                                  mission_id=Mission.objects.get(id=certification_data['mission_id']),
                                  owner=owner,
                                  content=certification_data.get('content', ''),
                                  img_urls=public_url_list,
                                  percieved_difficulty=certification_data['percieved_difficulty'])
    certification.save()
    return certification

def get_certifications_by_mission_id(mission_id):
    certification = Certification.objects.filter(mission_id=mission_id)
    return certification


# TODO : 인증 객체가 생기면 participation.status를 SUCCESS로 바꿈, user complete mission count, user participation count 갱신
def update_participation_by_certification(owner, mission_id):
    participation = get_participation_by_mission_and_owner(owner, mission_id)
    participation.status = Participation.Status.PARTICIPATED
    participation.save()

    return participation

# TODO : 기한 내에 인증 객체가 생기지 않았을 경우 participation.status를 FAILURE로 변경, READY로 다시 변경?
def update_participation_status_by_period(owner, mission_id):
    participation = get_participation_by_mission_and_owner(owner, mission_id)
    end_date= Participation.end_date
    now_date = datetime.now()
    if now_date > end_date:
        participation.status = Participation.Status.FAILURE
        participation.save()

    else:
        participation.status = Participation.Status.SUCCESS
        participation.save()

    return participation


def check_overlimit_certifications(owner, mission_id):
    participation = Participation.objects.get(owner=owner, status=Participation.Status.PARTICIPATED)
    if participation is True:
        return False
    else:
        return True

# TODO : 랭킹 기준으로 TOP 3
# def get_top3_ranker_user(owner, mission_id):
#     return

# 날짜 확인
# 재도전 시점? => 실패 status가 언제 ready로 바뀌게 되는가?
