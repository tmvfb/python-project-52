from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _

from .models import Label


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Name"),
                }
            )
        }
