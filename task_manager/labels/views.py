from django.shortcuts import redirect
from .models import Label
from .forms import LabelForm
from django.contrib import messages
from django.db.models import ProtectedError
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, ListView):

    model = Label
    paginate_by = 50
    template_name = 'labels/index.html'
    login_url = reverse_lazy('user_login')

    def get_queryset(self):
        return Label.objects.all().order_by('id')


class LabelCreateView(LoginRequiredMixin, CreateView):

    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('user_login')

    def form_valid(self, form):
        messages.success(self.request, _('Label created successfully!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        # adds bootstrap-js green checkmarks and red warning signs
        form.fields['name'].widget.attrs['class'] += ' is-invalid'
        messages.warning(self.request, _(
            'Something went wrong. Please check the entered data'
        ))
        return super().form_invalid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):

    form_class = LabelForm
    model = Label
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('user_login')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        messages.success(self.request, _('Label updated successfully!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        form.fields['name'].widget.attrs['class'] += ' is-invalid'
        messages.warning(self.request, _(
            'Something went wrong. Please check the entered data'
        ))
        return super().form_invalid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):

    model = Label
    success_url = reverse_lazy('labels')
    template_name = 'labels/delete.html'
    login_url = reverse_lazy('user_login')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        try:
            messages.success(self.request, _('Label deleted successfully!'))
            return super().form_valid(form)
        except ProtectedError:
            list(messages.get_messages(self.request))  # clear success message
            messages.warning(
                self.request,
                _('Label is connected with one or more tasks and cannot be deleted')  # noqa: E501
            )
            return redirect('labels')
