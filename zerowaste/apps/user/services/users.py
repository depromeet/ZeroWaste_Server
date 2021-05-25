from apps.core import exceptions
from apps.user.services.models import get_user_by_nickname

import logging


def nickname_double_check(user, nickname):
    if nickname:
        nickname_owner = get_user_by_nickname(nickname)
        if nickname_owner and nickname_owner.id != user.id:
            logging.debug(f"{nickname} is unavailable")
            raise exceptions.NicknameDoubleCheckedError()
        logging.debug(f"{nickname} is available")