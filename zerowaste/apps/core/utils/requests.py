import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from apps.core.exceptions import InternalServerError


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def requests_timeout(func, url, *args, **kwargs):
    """Handling timeout with retry-exception"""
    try:
        if 'timeout' not in kwargs.keys():
            kwargs['timeout'] = 3.0
        response = func(url, *args, **kwargs)
        return response
    except (requests.exceptions.RequestException, requests.exceptions.RetryError) as e:
        raise InternalServerError(str(e))


# def http_to_https(url):
#     if url.startswith('http://'):
#         url = url.replace('http://', 'https://', 1)
#     return url
