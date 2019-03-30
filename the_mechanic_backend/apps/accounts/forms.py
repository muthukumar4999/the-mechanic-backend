from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class MechanicUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)


class MechanicUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

