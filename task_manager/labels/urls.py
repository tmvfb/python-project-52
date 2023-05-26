from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='labels'),
    path('create/', views.LabelCreateView.as_view(), name='label_create'),
    path('<int:id>/update/', views.LabelUpdateView.as_view(), name='label_update'),  # noqa: E501
    path('<int:id>/delete/', views.LabelDeleteView.as_view(), name='label_delete'),  # noqa: E501
]
