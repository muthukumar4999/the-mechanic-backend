from django.contrib import admin
from django.contrib.auth.models import User

from the_mechanic_backend.apps.accounts.models import AuthUser, Store


class AuthUserAdmin(admin.ModelAdmin):
    model = AuthUser
    list_display = ['user', 'token', 'is_expired', 'created_at']

class StoreAdmin(admin.ModelAdmin):
    model = Store
    list_display = ['name', 'branch', 'type',]


admin.site.register(Store, StoreAdmin)
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.site_url = 'http://the-mechanic-backend.herokuapp.com/api/v0/docs/'