from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from the_mechanic_backend.apps.accounts.models import AuthUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            msg = 'Unable to login with required credentials'
            raise ValidationError(msg)
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ('token',)

#
#
# class CreateFileUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Media
#         fields = ('key', 'file_name', 'uploaded_at',)
#
#
# class GetFileSerializer(serializers.ModelSerializer):
#     url = serializers.SerializerMethodField()
#
#     def get_url(self, obj):
#         return settings.AWS_S3_BASE_LINK + obj.key
#
#     class Meta:
#         model = Media
#         fields = ('id', 'file_name', 'url', 'key',)
#
#
# class BasicUserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'user_type', 'phone_number')
#
#
