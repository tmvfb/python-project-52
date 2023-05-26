from django.shortcuts import redirect
from .models import Status
from .forms import StatusForm
from django.contrib import messages
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, ListView):

    model = Status
    paginate_by = 50
    template_name = 'statuses/index.html'
    login_url = reverse_lazy('user_login')

    def get_queryset(self):
        return Status.objects.all().order_by('id')


class StatusCreateView(LoginRequiredMixin, CreateView):

    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('user_login')

    def form_valid(self, form):
        messages.success(self.request, _('Status created successfully!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        # adds bootstrap-js green checkmarks and red warning signs
        form.fields['name'].widget.attrs['class'] += ' is-invalid'
        messages.warning(self.request, _(
            'Something went wrong. Please check the entered data'
        ))
        return super().form_invalid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):

    form_class = StatusForm
    model = Status
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('user_login')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        messages.success(self.request, _('Status updated successfully!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        form.fields['name'].widget.attrs['class'] += ' is-invalid'
        messages.warning(self.request, _(
            'Something went wrong. Please check the entered data'
        ))
        return super().form_invalid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):

    model = Status
    success_url = reverse_lazy('statuses')
    template_name = 'statuses/delete.html'
    login_url = reverse_lazy('user_login')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        try:
            messages.success(self.request, _('Status deleted successfully!'))
            return super().form_valid(form)
        except ProtectedError:
            list(messages.get_messages(self.request))  # clear success message
            messages.warning(
                self.request,
                _('Status is connected with one or more tasks and cannot be deleted')  # noqa: E501
            )
            return redirect('statuses')
