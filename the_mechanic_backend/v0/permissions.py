from rest_framework import status
from rest_framework.exceptions import APIException

from the_mechanic_backend.validator.errorcodemapping import ErrorMessage
from the_mechanic_backend.validator.errormapping import ErrorCode


class UnauthorizedAccess(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"message": ErrorMessage.UNAUTHORIZED_ACCESS, "status": "failed",
                      "code": ErrorCode.UNAUTHORIZED_ACCESS}
