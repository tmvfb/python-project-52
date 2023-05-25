from .models import Task
from django.forms import ModelForm, TextInput, Textarea, Select
from django.utils.translation import gettext_lazy as _


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'assigned_to'
        ]
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name'),
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': _('Description'),
            }),
            'status': Select(attrs={
                'class': 'form-control form-select',
                'placeholder': _('Status'),
            }),
            'assigned_to': Select(attrs={
                'class': 'form-control form-select',
                'placeholder': _('Assignee'),
            })
        }
