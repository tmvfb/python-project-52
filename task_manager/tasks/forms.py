from .models import Task
from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name'),
            })
        }
