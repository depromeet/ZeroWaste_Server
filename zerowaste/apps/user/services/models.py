from apps.user.models.user import User
from apps.user.models.auth import Auth
from apps.core.utils.tools import id_generator


def create_anonymous_user():
    user = User(nickname=id_generator())
    user.save()
    return user


def get_auth_by_identifier_with_login_type(identifier, login_type):
    auth = Auth.objects.get(identifier=str(identifier), login_type=login_type)
    return auth


def create_auth(identifier, email, user, social_token, login_type):
    auth = Auth(identifier=str(identifier), email=email, user_id=user, social_token=social_token,
                login_type=login_type)
    auth.save()
    return auth