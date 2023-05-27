from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.mixins import MessagesDeleteProtectedMixin, MessagesMixin

from .forms import LabelForm
from .models import Label


class IndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    login_url = reverse_lazy('user_login')
    paginate_by = 50

    def get_queryset(self):
        return Label.objects.all().order_by('id')


class LabelCreateView(MessagesMixin, LoginRequiredMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/create.html'

    success_message = _("Label created successfully!")

    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('user_login')


class LabelUpdateView(MessagesMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'

    success_message = _("Label updated successfully!")

    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('user_login')
    pk_url_kwarg = 'id'


class LabelDeleteView(
    MessagesDeleteProtectedMixin,
    LoginRequiredMixin,
    DeleteView
):
    model = Label
    template_name = 'labels/delete.html'

    success_message = _("Label deleted successfully!")
    error_message_protected = _("Label is connected with one or more tasks and cannot be deleted")  # noqa: E501

    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('user_login')
    redirect_url = "labels"
    pk_url_kwarg = 'id'
