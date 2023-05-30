from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from task_manager.mixins import MessagesMixin, UserPermissionMixin

from .forms import FilterForm, TaskForm
from .models import Task


class IndexView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/index.html"
    login_url = reverse_lazy("user_login")
    paginate_by = 50

    def get_queryset(self):
        tasks = Task.objects.all().order_by("id")
        if 'Reset' in self.request.GET:
            return tasks
        self.filters = {
            "status": self.request.GET.get("status"),
            "executor": self.request.GET.get("executor"),
            "labels": self.request.GET.get("labels"),
            "mine": self.request.GET.get("mine"),
        }

        # custom filtering by several fields
        for var_name, filter in self.filters.items():
            if var_name == "mine" and filter:
                tasks = tasks.filter(assigned_by=self.request.user.id)
            elif filter:
                kwargs = {var_name: filter}
                tasks = tasks.filter(**kwargs)

        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FilterForm()

        # populate form fields with current selected values
        for form_field, value in self.filters.items():
            context["form"].fields[form_field].initial = value
        return context


class TaskCreateView(MessagesMixin, LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = "tasks/create.html"

    success_message = _("Task created successfully")

    success_url = reverse_lazy("tasks")
    login_url = reverse_lazy("user_login")

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.assigned_by = User.objects.get(
            username=self.request.user.username
        )
        candidate.save()  # set current user as task creator
        return super().form_valid(form)


class TaskUpdateView(MessagesMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"

    success_message = _("Task updated successfully")

    success_url = reverse_lazy("tasks")
    login_url = reverse_lazy("user_login")
    pk_url_kwarg = "id"


class TaskDeleteView(
    MessagesMixin,
    LoginRequiredMixin,
    UserPermissionMixin,
    DeleteView
):
    model = Task
    template_name = "tasks/delete.html"

    success_message = _("Task deleted successfully")
    error_message_permission = _("Only the creator of the task can delete it")

    success_url = reverse_lazy("tasks")
    login_url = reverse_lazy("user_login")
    redirect_url = "tasks"
    pk_url_kwarg = "id"


class TaskShowView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/show.html"
    login_url = reverse_lazy("user_login")
    pk_url_kwarg = "id"
