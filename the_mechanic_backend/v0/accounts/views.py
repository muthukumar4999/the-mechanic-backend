from django.http import HttpResponse
from rest_framework.permissions import AllowAny

from the_mechanic_backend.apps.accounts.models import AuthUser, Store
from the_mechanic_backend.v0.accounts import serializers, forms
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


class XlsFileUpload(CustomBaseClass):
    def post(self, request, *args, **kwargs):
        xls_file = forms.FileUploadForm(request.POST, request.FILES)
        if xls_file.is_valid():
            return HttpResponse("Success")
        return HttpResponse("file Upload Failed")


class StoreList(CustomBaseClass):
    def get(self, request, *args, **kwargs):
        try:
            st = self.get_all_objects(Store)
            serializer = serializers.StoreSerializer(st, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
           return self.internal_server_error(request, e)

    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            serializer = serializers.StoreSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, 'VALIDATION_ERROR', serializer.data)
            return Utils.dispatch_failure(request, serializer.errors)
        except Exception as e:
            print(e)
            return self.internal_server_error(request, e)
