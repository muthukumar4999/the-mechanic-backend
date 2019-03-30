from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MechanicUserChangeForm, MechanicUserCreationForm
from the_mechanic_backend.apps.accounts.models import AuthUser, Store, User


class MechanicUserAdmin(UserAdmin):
    add_form = MechanicUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )
    form = MechanicUserChangeForm
    list_display = ('username', 'email', 'role', 'store')
    fieldsets = UserAdmin.fieldsets + \
                (
                    ('Other info', {'fields': ('role',
                                               'store',)}),
                )
    readonly_fields = ('last_login', 'date_joined',)


class AuthUserAdmin(admin.ModelAdmin):
    model = AuthUser
    list_display = ['user', 'token', 'is_expired', 'created_at']


class StoreAdmin(admin.ModelAdmin):
    model = Store
    list_display = ['name', 'branch', 'type', ]


admin.site.register(User, MechanicUserAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.site_url = 'http://the-mechanic-backend.herokuapp.com/api/v0/docs/'
