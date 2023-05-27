from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {
                "maxlength": "50",
                "class": "form-control",
                "placeholder": _("First name"),
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "maxlength": "50",
                "class": "form-control",
                "placeholder": _("Last name"),
            }
        )
        self.fields["username"].widget.attrs.update(
            {
                "maxlength": "50",
                "class": "form-control",
                "placeholder": _("Username"),
            }
        )
        self.fields["username"].help_text = _(
            "Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."  # noqa: E501
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": _("Password")}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": _("Repeat password")}
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})
