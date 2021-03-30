from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from . import errno


class CoreException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = errno.INTERNAL_SERVER_ERROR
    user_message = None
    redirect_url = None

    def __init__(self, detail=None, code=None, user_message=None, redirect_url=None):
        super(CoreException, self).__init__(detail=detail, code=code)
        if user_message:
            self.user_message = user_message
        if redirect_url:
            self.redirect_url = redirect_url

    def as_md(self):
        """for swagger markdown rendering"""
        return '\n\n> **%s**\n\n```\n{\n\n\t"code": "%s"\n\n\t"message": "%s"\n\n}\n\n```' % \
               (self.default_code, self.status_code, self.default_detail)


class BadRequest(CoreException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad request.')
    default_code = errno.BAD_REQUEST


class ValidationError(BadRequest):
    default_detail = _('Invalid input.')
    default_code = errno.VALIDATION_ERROR


class Unauthorized(CoreException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Unauthorized.')
    default_code = errno.UNAUTHORIZED


class InternalServerError(CoreException):
    """Uncaught error for 500"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A Internal server error occurred.')
    default_code = errno.INTERNAL_SERVER_ERROR
