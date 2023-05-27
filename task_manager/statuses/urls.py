from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='statuses'),
    path('create/', views.StatusCreateView.as_view(), name='status_create'),
    path('<int:id>/update/', views.StatusUpdateView.as_view(), name='status_update'),  # noqa: E501
    path('<int:id>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),  # noqa: E501
]
