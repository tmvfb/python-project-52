from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.mixins import MessagesDeleteProtectedMixin, MessagesMixin

from .forms import StatusForm
from .models import Status


class IndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    login_url = reverse_lazy("user_login")
    paginate_by = 50

    def get_queryset(self):
        return Status.objects.all().order_by("id")


class StatusCreateView(MessagesMixin, LoginRequiredMixin, CreateView):
    form_class = StatusForm
    template_name = "statuses/create.html"

    success_message = _("Status created successfully!")

    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("user_login")


class StatusUpdateView(MessagesMixin, LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"

    success_message = _("Status updated successfully!")

    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("user_login")
    pk_url_kwarg = "id"


class StatusDeleteView(
    MessagesDeleteProtectedMixin,
    LoginRequiredMixin,
    DeleteView
):
    model = Status
    template_name = "statuses/delete.html"

    success_message = _("Status deleted successfully!")
    error_message_protected = _("Status is connected with one or more tasks and cannot be deleted")  # noqa: E501

    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("user_login")
    redirect_url = "statuses"
    pk_url_kwarg = "id"
