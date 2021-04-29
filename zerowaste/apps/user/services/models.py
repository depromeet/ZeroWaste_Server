from apps.user.models.user import User
from apps.user.models.auth import Auth
from apps.core.utils.tools import id_generator
from apps.user.services.jwt_token import get_user_token


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


def get_user_by_id(user_id):
    user = User.objects.get(id=user_id)
    return user


def record_user_token(auth):
    # TODO: auth의 user_id가 user object를 들고있는데, 확인하기
    token = get_user_token(get_user_by_id(auth.user_id.id))
    auth.token = token
    auth.save()
    return auth
