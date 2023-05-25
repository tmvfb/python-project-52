from .models import Task
from django import forms
from django.forms import ModelForm, TextInput, Textarea, Select, CheckboxInput
from django.utils.translation import gettext_lazy as _


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor'
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
            'executor': Select(attrs={
                'class': 'form-control form-select',
                'placeholder': _('Assignee'),
            })
        }


class FilterForm(ModelForm):

    mine = forms.BooleanField(label=_('Is mine'))

    class Meta:
        model = Task
        fields = [
            'status',
            'executor',
            'mine'
        ]
        widgets = {
            'status': Select(attrs={
                'class': 'form-control form-select',
                'placeholder': _('Status'),
            }),
            'executor': Select(attrs={
                'class': 'form-control form-select',
                'placeholder': _('Assignee'),
            }),
            'mine': CheckboxInput(attrs={
                'class': 'form-check-input',
                'placeholder': _('Is my task'),
            })
        }
