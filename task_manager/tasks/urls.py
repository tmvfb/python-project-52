from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='tasks'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:id>/update/', views.TaskUpdateView.as_view(), name='task_update'),  # noqa: E501
    path('<int:id>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),  # noqa: E501
    path('<int:id>/', views.TaskShowView.as_view(), name='task_show'),
]
