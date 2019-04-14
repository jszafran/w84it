from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.utils.translation import gettext_lazy as _

class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username')
        labels = {
            'username': _('Username'),
        }


class UserChangeForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm):
        model = User
        fields = ('first_name', 'last_name', 'username',)
        labels = {
            'username': _('Username'),
        }

