from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.exceptions import APIException

from the_mechanic_backend.apps.accounts.models import AuthUser
from the_mechanic_backend.validator.errorcodemapping import ErrorMessage
from the_mechanic_backend.validator.errormapping import ErrorCode


class UnauthorizedAccess(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"message": ErrorMessage.UNAUTHORIZED_ACCESS, "status": "failed",
                      "code": ErrorCode.UNAUTHORIZED_ACCESS}


class CustomAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if username and password:
                user = User._default_manager.get_by_natural_key(username)
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
                else:
                    return None
            else:
                authorization = request.META['HTTP_AUTHORIZATION']
                if not authorization:
                    return None
                else:
                    token = authorization.split(' ')[1]
                    try:
                        return (AuthUser.objects.get(token=token, is_expired=False).user, None)
                    except AuthUser.DoesNotExist:
                        return None
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
