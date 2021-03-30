import logging
import sys
import traceback
from typing import Union

from django.conf import settings
from django.http import HttpRequest
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import exceptions as drf_exceptions
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import exception_handler

from . import trace_log
from ..exceptions import CoreException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context=None):
    """
    참고: https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
    """
    if context:
        request = context['request']
        request_id = request.META.get('request_id')
    else:
        request = None
        request_id = None

    logger.debug(f'req & req_id: {request, request_id}')
    logger.debug(f'exc: {exc}')

    if not _is_log_excluded_exception(exc):
        trace_log.error(
            request=request,
            data={
                'message': str(exc),
                'request_id': request_id},
            exc_info=True)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    logger.debug(f'response: {response}')

    if response is not None:
        response.data = build_error_data(exc)
        return response

    if settings.ENVIRONMENT == 'PRODUCTION':
        internal_error_message = str(exc)
    else:
        exc_type, _, _ = sys.exc_info()
        internal_error_message = str(traceback.format_exc()) if exc_type else str(exc)

    internal_exc = CoreException(detail=internal_error_message)
    return Response(build_error_data(internal_exc, error_id=request_id),
                    status=internal_exc.status_code)


def _is_log_excluded_exception(exc):
    if (isinstance(exc, drf_exceptions.ValidationError) or
            isinstance(exc, drf_exceptions.NotFound)):
        return True
    return False


def build_error_data(exc, error_id=None):
    error_response = {
        'message': None,
        'error_code': None,
        'user_msg': None,
        'error_id': None,
        'redirect_url': None
    }

    if isinstance(exc, CoreException):
        error_response.update({
            'message': str(exc.detail),
            'error_code': exc.detail.code,
            'user_msg': getattr(exc, 'user_message', None),
            'error_id': error_id,
            'redirect_url': getattr(exc, 'redirect_url', None)
        })
    elif isinstance(exc, APIException):
        error_response.update({
            'message': str(exc),
            'error_code': exc.status_code,
            'error_id': error_id,
        })
    else:
        error_response.update({
            'message': str(exc),
            'error_code': CoreException.status_code,
            'error_id': error_id,
        })

    return _remove_none_value_keys(error_response)


def _remove_none_value_keys(dict_obj):
    return type(dict_obj)([(key, dict_obj[key]) for key in dict_obj if dict_obj[key] is not None])


def list_of_int(s):
    return [int(n.strip()) for n in s.split(',')]


def list_of_str(s):
    return [p.strip() for p in s.split(',')]


def boolean(val):
    return val in {'True', 'true', '1', True, 1}


def get_validated_params(request: Union[HttpRequest, Request], validation_spec: dict):
    validated_params = {}
    for name, spec in validation_spec.items():
        try:
            is_default_value = False

            if spec.get('required', True):
                value = request.GET[name]
            else:
                default = spec['default']
                if name in request.GET:
                    value = request.GET[name]
                else:
                    value = default
                    is_default_value = True

            conv_type = spec.get('type')
            if conv_type and not is_default_value:
                value = conv_type(value)

            if spec.get('choices') and value not in spec.get('choices'):
                raise drf_exceptions.ValidationError(
                    detail='"{}={}" is not a valid value'.format(name, value))

            validated_params[name] = value
        except drf_exceptions.ValidationError as e:
            raise e
        except MultiValueDictKeyError as e:
            raise drf_exceptions.ValidationError(detail='%s cannot be empty.' % name)
        except Exception as e:
            raise drf_exceptions.ValidationError(
                detail='{} is invalid value. (why: {})'.format(name, str(e)))

    return validated_params
