from django.contrib import admin
from django.contrib.auth.models import User

from the_mechanic_backend.apps.accounts.models import AuthUser


class AuthUserAdmin(admin.ModelAdmin):
    model = AuthUser
    list_display = ['user', 'token', 'is_expired', 'created_at']


admin.site.register(AuthUser, AuthUserAdmin)
