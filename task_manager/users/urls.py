from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.IndexView.as_view(), name='users'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:id>/update/', views.UserUpdateView.as_view(), name='user_update'),  # noqa: E501
    path('<int:id>/delete/', views.UserDeleteView.as_view(), name='user_delete'),  # noqa: E501
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]
