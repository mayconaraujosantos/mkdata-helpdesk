from rest_framework.exceptions import APIException

from account import messages


class PermissionNotAllowedException(APIException):
    status_code = 403
    default_detail = messages.PERMISSION_NOT_ALLOWED


class InvalidPasswordException(APIException):
    status_code = 405
    default_detail = messages.INVALID_PASSWORD
