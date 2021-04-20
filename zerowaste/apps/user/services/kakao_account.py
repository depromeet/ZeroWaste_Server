import requests

from apps.core.exceptions import KakaoAccountServerError


def get_user_profile(kakao_access_token):
    url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization': 'Bearer ' + kakao_access_token}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise KakaoAccountServerError(detail=response.json()['msg'])

    return response.json()
