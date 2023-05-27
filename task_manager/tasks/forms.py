from django import forms
from django.contrib.auth.models import User
from django.forms import (
    CheckboxInput,
    ModelForm,
    Select,
    SelectMultiple,
    Textarea,
    TextInput,
)
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label

from .models import Task


class CustomModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
    listed as 'first_name last_name' instead of just
    'username'.
    """

    def label_from_instance(self, obj):
        return obj.get_full_name()


class TaskForm(ModelForm):
    executor = CustomModelChoiceField(
        queryset=User.objects.all(),
        label=_("Assignee"),
        required=False,
        widget=Select(
            attrs={
                "class": "form-control form-select",
            }
        ),
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        label=_("Labels"),
        required=False,
        widget=SelectMultiple(
            attrs={
                "class": "form-control form-select",
                "placeholder": _("Label"),
                "multiple": True,
            }
        ),
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Name"),
                }
            ),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Description"),
                }
            ),
            "status": Select(
                attrs={
                    "class": "form-control form-select",
                    "placeholder": _("Status"),
                }
            ),
        }


class FilterForm(ModelForm):
    mine = forms.BooleanField(label=_("Is mine"))

    # had to rewrite as default doesn't provide empty choice
    # can use ModelMultipleChoiceField as well
    labels = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        label=_("Label"),
        required=False,
        widget=Select(
            attrs={
                "class": "form-control form-select",
            }
        ),
    )
    executor = CustomModelChoiceField(
        queryset=User.objects.all(),
        label=_("Assignee"),
        required=False,
        widget=Select(
            attrs={
                "class": "form-control form-select",
            }
        ),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "mine"]
        widgets = {
            "status": Select(
                attrs={
                    "class": "form-control form-select",
                    "placeholder": _("Status"),
                }
            ),
            "mine": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "placeholder": _("Is my task"),
                }
            ),
        }
