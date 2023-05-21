from django.forms import (
    TextInput, Textarea, ValidationError,
    CharField, PasswordInput
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class RegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'maxlength': '50',
            'class': 'form-control',
            'placeholder': _('First name')
        })
        self.fields['last_name'].widget.attrs.update({
            'maxlength': '50',
            'class': 'form-control',
            'placeholder': _('Last name')
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Username')
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Repeat password')
        })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
