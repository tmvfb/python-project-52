from django.shortcuts import redirect
from .models import Status
from .forms import StatusForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class CheckStatusMixin(UserPassesTestMixin):  # TODO
    '''
    Checks if the status is assigned to any task.
    '''
    error_message = None
    redirect_url = reverse_lazy('statuses')

    def handle_no_permission(self):
        return redirect(self.redirect_url)

    def test_func(self):
        # status_id = self.kwargs.get('id')
        # status = get_object_or_404(Status, id=status_id)
        if False:  # TODO
            messages.warning(self.request, _(self.error_message))
            return False
        return True


class IndexView(LoginRequiredMixin, ListView):

    model = Status
    paginate_by = 50
    template_name = 'statuses/index.html'
    login_url = reverse_lazy('user_login')

    def get_queryset(self):
        return Status.objects.all().order_by('pk')


class StatusCreateView(LoginRequiredMixin, CreateView):

    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy('user_login')

    def form_valid(self, form):
        messages.success(self.request, _("Status created successfully!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        # adds bootstrap-js green checkmarks and red warning signs
        form.fields['name'].widget.attrs['class'] += ' is-invalid'
        messages.warning(self.request, _(
            "Something went wrong. Please check the entered data"
        ))
        return super().form_invalid(form)


class StatusUpdateView(LoginRequiredMixin, CheckStatusMixin, UpdateView):

    # TODO: status already exists message

    form_class = StatusForm
    model = Status
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy('user_login')
    error_message = _("This status is assigned to one or more tasks and can not be updated")  # noqa: E501
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        messages.success(self.request, _("Status updated successfully!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        form.fields['name'].widget.attrs['class'] += ' is-invalid'
        messages.warning(self.request, _(
            "Something went wrong. Please check the entered data"
        ))
        return super().form_invalid(form)


class StatusDeleteView(LoginRequiredMixin, CheckStatusMixin, DeleteView):

    model = Status
    success_url = reverse_lazy('statuses')
    template_name = 'statuses/delete.html'
    login_url = reverse_lazy('user_login')
    error_message = _("This status is assigned to one or more tasks and can not be deleted")  # noqa: E501
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        messages.success(self.request, _('Status deleted successfully!'))
        return super().form_valid(form)