from django.shortcuts import redirect
from .models import Task
from .forms import TaskForm, FilterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DeleteView, CreateView, UpdateView, ListView, DetailView
)
from django.urls import reverse_lazy
from django.contrib.sessions.backends.db import SessionStore
from django.utils.translation import gettext_lazy as _


class IndexView(LoginRequiredMixin, ListView):

    model = Task
    paginate_by = 50
    template_name = 'tasks/index.html'
    login_url = reverse_lazy('user_login')

    def get_queryset(self):
        tasks = Task.objects.all().order_by('id')
        self.filters = {
            'status': self.request.GET.get('status'),
            'executor': self.request.GET.get('executor'),
            'labels': self.request.GET.get('labels'),
            'mine': self.request.GET.get('mine')
        }

        # custom filtering by several fields
        for var_name, filter in self.filters.items():
            if var_name == 'mine' and filter:
                tasks = tasks.filter(
                    assigned_by=self.request.user.id
                )
            elif filter:
                kwargs = {var_name: filter}
                tasks = tasks.filter(**kwargs)

        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm()

        # populate form fields with current selected values
        for form_field, value in self.filters.items():
            context['form'].fields[form_field].initial = value
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):

    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('user_login')

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.assigned_by = User.objects.get(
            username=self.request.user.username
        )
        candidate.save()  # set current user as task creator
        messages.success(self.request, _('Task created successfully!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        # adds bootstrap-js green checkmarks and red warning signs
        for field in form:
            if field.errors:
                form.fields[field.name].widget.attrs['class'] += ' is-invalid'
            else:
                form.fields[field.name].widget.attrs['class'] += ' is-valid'
        messages.warning(self.request, _(
            'Something went wrong. Please check the entered data'
        ))
        return super().form_invalid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):

    form_class = TaskForm
    model = Task
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('user_login')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        messages.success(self.request, _('Task updated successfully!'))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            if field.errors:
                form.fields[field.name].widget.attrs['class'] += ' is-invalid'
            else:
                form.fields[field.name].widget.attrs['class'] += ' is-valid'
        messages.warning(self.request, _(
            'Something went wrong. Please check the entered data'
        ))
        return super().form_invalid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/delete.html'
    login_url = reverse_lazy('user_login')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        messages.success(self.request, _('Task deleted successfully!'))
        return super().form_valid(form)

    def handle_no_permission(self):
        return redirect('tasks')

    def test_func(self):
        user_id = self.request.user.id
        creator_id = self.get_object().assigned_by.id
        if user_id != creator_id:
            messages.warning(
                self.request, _('Only the creator of the task can delete it')
            )
            return False
        return True


class TaskShowView(LoginRequiredMixin, DetailView):

    model = Task
    pk_url_kwarg = 'id'
    template_name = 'tasks/show.html'
    login_url = reverse_lazy('user_login')
