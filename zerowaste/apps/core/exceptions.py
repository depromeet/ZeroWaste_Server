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


# 서비스적인 Exception은 200을 보내고, error_code로 핸들링
class ServiceException(CoreException):
    status_code = status.HTTP_200_OK
    default_detail = _('A server error occurred.')


class BadRequest(ServiceException):
    default_detail = _('Bad request.')
    default_code = errno.BAD_REQUEST


class ValidationError(BadRequest):
    default_detail = _('Invalid input.')
    default_code = errno.VALIDATION_ERROR


class Unauthorized(ServiceException):
    default_detail = _('Unauthorized.')
    default_code = errno.UNAUTHORIZED


class InternalServerError(ServiceException):
    default_detail = _('A Internal server error occurred.')
    default_code = errno.INTERNAL_SERVER_ERROR


class SoftDeleteError(CoreException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Soft delete error.')
    default_code = errno.SOFT_DELETE_ERROR
