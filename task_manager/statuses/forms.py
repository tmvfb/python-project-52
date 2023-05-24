from .models import Status
from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name'),
            })
        }
