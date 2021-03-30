import logging
import socket
import inspect

import ujson
from django.conf import settings

_logger = logging.getLogger('core.trace_log')


def log(level,
        request=None,
        response=None,
        data=None,
        **kwargs):
    # _tmp_debug(level, request, response, data, **kwargs)

    t = {
        'phase': settings.ENVIRONMENT,
        'hostname': socket.getfqdn()
    }

    stack = inspect.stack()
    if len(stack) >= 2:
        t['filename'] = stack[2].filename
        t['function'] = stack[2].function

    if request:
        t['method'] = request.method
        t['path'] = request.path
        if request.META and 'request_id' in request.META:
            t['request_id'] = request.META['request_id']

        headers = {k: v for k, v in request.META.items() if k.startswith('HTTP_')}

        '''
        if 'HTTP_AUTHORIZATION' in headers:
            auth = headers['HTTP_AUTHORIZATION'].split()
            if len(auth) == 1:
                headers.pop('HTTP_AUTHORIZATION')
            elif len(auth) == 2:
                if auth[0].lower() == 'token':
                    headers.pop('HTTP_AUTHORIZATION')
            else:
                pass
        '''

        if headers:
            t['headers'] = headers

        if request.POST:
            content_type = request.META.get('CONTENT_TYPE', '')
            if content_type == 'application/json':
                t['post'] = request.POST

    if response:
        t['response_status_code'] = response.status_code

    if hasattr(response, 'data') and response.data and getattr(response.data, 'error', False):
        t['original_error'] = response.data.get('error')

    if data is not None:
        assert (isinstance(data, dict))
        if 'request_id' in data:
            t['request_id'] = data['request_id']
        t.update(data)

    try:

        json_log = ujson.dumps(t)

    except Exception as e:
        err_data = {'message': 'Cannot convert to JSON', 'data': str(t)}
        try:
            err_json = ujson.dumps(err_data)
            return _logger.log(logging.ERROR, err_json, **kwargs)
        except:
            return _logger.log(logging.ERROR, err_data, **kwargs)
    else:
        return _logger.log(level, json_log, **kwargs)


def error(request=None, response=None, data=None, **kwargs):
    return log(logging.ERROR, request=request, response=response, data=data, **kwargs)


def info(request=None, response=None, data=None, **kwargs):
    return log(logging.INFO, request=request, response=response, data=data, **kwargs)


def _tmp_debug(level, request, response, data, **kwargs):
    _logger.info(f"debug(level): {level}")
    _logger.info(f"debug(request): {request}")
    _logger.info(f"debug(response): {response}")

    if hasattr(response, 'data'):
        _logger.info(f"debug(response.data): {response.data}")

    if hasattr(response, 'content'):
        _logger.info(f"debug(response.content): {response.content}")
    else:
        _logger.info(f"debug(dir(response): {dir(response)}")

    _logger.info(f"debug(data): {data}")
    _logger.info(f"debug(**kwargs): {kwargs}")
