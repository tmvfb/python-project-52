from django.shortcuts import redirect
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class CheckTaskMixin(UserPassesTestMixin):  # TODO
    '''
    Checks if the task is assigned to any task.
    '''
    error_message = None
    redirect_url = reverse_lazy('tasks')

    def handle_no_permission(self):
        return redirect(self.redirect_url)

    def test_func(self):
        # task_id = self.kwargs.get('id')
        # task = get_object_or_404(Task, id=task_id)
        if False:  # TODO
            messages.warning(self.request, _(self.error_message))
            return False
        return True


class IndexView(LoginRequiredMixin, ListView):

    model = Task
    paginate_by = 50
    template_name = 'tasks/index.html'
    login_url = reverse_lazy('user_login')

    def get_queryset(self):
        return Task.objects.all().order_by('pk')


class TaskCreateView(LoginRequiredMixin, CreateView):

    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks")
    login_url = reverse_lazy('user_login')

    def form_valid(self, form):
        messages.success(self.request, _("Task created successfully!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        # adds bootstrap-js green checkmarks and red warning signs
        form.fields['name'].widget.attrs['class'] += ' is-invalid'
        messages.warning(self.request, _(
            "Something went wrong. Please check the entered data"
        ))
        return super().form_invalid(form)


class TaskUpdateView(LoginRequiredMixin, CheckTaskMixin, UpdateView):

    # TODO: task already exists message

    form_class = TaskForm
    model = Task
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks")
    login_url = reverse_lazy('user_login')
    error_message = _("This task is assigned to one or more tasks and can not be updated")  # noqa: E501
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        messages.success(self.request, _("Task updated successfully!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        form.fields['name'].widget.attrs['class'] += ' is-invalid'
        messages.warning(self.request, _(
            "Something went wrong. Please check the entered data"
        ))
        return super().form_invalid(form)


class TaskDeleteView(LoginRequiredMixin, CheckTaskMixin, DeleteView):

    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/delete.html'
    login_url = reverse_lazy('user_login')
    error_message = _("This task is assigned to one or more tasks and can not be deleted")  # noqa: E501
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        messages.success(self.request, _('Task deleted successfully!'))
        return super().form_valid(form)
