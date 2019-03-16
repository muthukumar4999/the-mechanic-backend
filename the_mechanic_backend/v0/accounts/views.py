from rest_framework.permissions import AllowAny

from the_mechanic_backend.apps.accounts.models import AuthUser
from the_mechanic_backend.v0.accounts import serializers
from the_mechanic_backend.v0.utils import Utils, CustomBaseClass


class LoginView(CustomBaseClass):
    """
       Login View allows the user to login into the application
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        To verify the authorized user and login them to the application
        :param request:
        :return:
        """
        validate_user = serializers.LoginSerializer(data=request.data)
        if validate_user.is_valid():
            user = validate_user.validated_data
            old_tokens = self.get_filter_objects(AuthUser, user=user, is_expired=True)
            if old_tokens:
                old_tokens.delete()

            self.get_filter_objects(AuthUser, user=user).update(is_expired=True)
            new_session = AuthUser(user=user)
            new_session.token = Utils.generate_token()
            new_session.save()
            serializer = serializers.AuthUserSerializer(new_session)
            return Utils.dispatch_success(request, serializer.data)
        else:
            return Utils.dispatch_failure(request, "UNAUTHORIZED_ACCESS", validate_user.errors)
