from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class UserPermissionMixin(UserPassesTestMixin):
    """
    Checks if user tries to update or delete other user's profile or task.
    Sends a flash if user is not authenticated.
    """
    # error_message_permission = None
    # error_message_login = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _(self.error_message_login)
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect(self.redirect_url)

    def test_func(self):
        if 'users/' in self.request.path:  # case delete users
            user_id = self.kwargs.get("id")  # id of user to be deleted
        else:  # case delete tasks
            user_id = self.get_object().assigned_by.id  # get task creator id

        current_user = self.request.user
        if (current_user.id != user_id) and not current_user.is_superuser():
            messages.error(self.request, _(self.error_message_permission))
            return False
        return True


class MessagesMixin:
    """
    Redefines validation functions to show flash messages.
    Adds bootstrap-js green checkmarks and red warning signs for forms.
    """
    # success_message = None

    def form_valid(self, form):
        messages.success(
            self.request, _(self.success_message)
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            if field.errors:
                form.fields[field.name].widget.attrs["class"] += " is-invalid"
            else:
                form.fields[field.name].widget.attrs["class"] += " is-valid"
        messages.error(
            self.request,
            _("Something went wrong. Please check the entered data"),
        )
        return super().form_invalid(form)


class MessagesDeleteProtectedMixin:
    """
    Redefines validation function to show flash messages
    and cover ProtectedError.
    """
    # success_message = None
    # error_message_protected = None

    def form_valid(self, form):
        try:
            messages.success(
                self.request, _(self.success_message)
            )
            return super().form_valid(form)
        except ProtectedError:
            list(messages.get_messages(self.request))  # clear success message
            messages.error(
                self.request, _(self.error_message_protected),
            )
            return redirect(self.redirect_url)
