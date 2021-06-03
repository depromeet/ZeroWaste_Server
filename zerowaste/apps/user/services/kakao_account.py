from apps.core.utils.requests import requests_timeout,requests_retry_session
from apps.core.exceptions import KakaoAccountServerError


def get_user_profile(kakao_access_token):
    url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization': 'Bearer ' + kakao_access_token}
    response = requests_timeout(requests_retry_session().get,
                                url=url,
                                headers=headers,
                                timeout=3)

    if response.status_code != 200:
        raise KakaoAccountServerError(detail=response.json()['msg'])

    return response.json()
