from apps.mission.services.models import get_participations_after_end_date
from apps.mission.models.participation import Participation
from apps.mission.models.mission import Mission
from apps.core.exceptions import BatchProcessError

import logging
logger = logging.getLogger(__name__)


def update_participation_status():
    try:
        logger.info("cronjob is working")
        participated_querysets = get_participations_after_end_date(status=Participation.Status.READY)
        for participated_queryset in participated_querysets:
            logger.debug(f'{participated_queryset}')
            participated_queryset.status = Participation.Status.SUCCESS
            participated_queryset.is_cron_checked = True

        Participation.objects.bulk_update(participated_querysets, ['status', 'is_cron_checked'])

        # ready_querysets = get_participations_after_end_date(status=Participation.Status.READY)

        missions = Mission.objects.all()
        for mission in missions:
            logger.info(f"Before : {mission.successful_count}, {mission.in_progress_count}")
            mission.update_successful_count()
            mission.update_in_progress_count()
            logger.info(f"After : {mission.successful_count}, {mission.in_progress_count}")
    except Exception:
        raise BatchProcessError()
