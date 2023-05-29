# from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class HomePageView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "base.html")


class SearchView(ListView):
    model = User
    template_name = "search.html"
    context_object_name = "users"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = User.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        query_statuses = Status.objects.filter(
            Q(name__icontains=query)
        ).order_by("id")
        query_labels = Label.objects.filter(
            Q(name__icontains=query)
        ).order_by("id")
        query_tasks = Task.objects.filter(
            Q(name__icontains=query)
            | Q(status__name__icontains=query)
            | Q(assigned_by__first_name__icontains=query)
            | Q(assigned_by__last_name__icontains=query)
            | Q(executor__first_name__icontains=query)
            | Q(executor__last_name__icontains=query)
        ).order_by("id")

        context.update(
            {
                "statuses": query_statuses,
                "labels": query_labels,
                "tasks": query_tasks,
            }
        )
        return context
