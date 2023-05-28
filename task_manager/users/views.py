from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.mixins import (
    MessagesDeleteProtectedMixin,
    MessagesMixin,
    UserPermissionMixin,
)

from .forms import LoginForm, RegistrationForm


class IndexView(ListView):
    model = User
    template_name = "users/index.html"
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(is_superuser=False).order_by("pk")


class UserCreateView(MessagesMixin, CreateView):
    form_class = RegistrationForm
    template_name = "users/create.html"

    success_message = _("User created successfully!")

    success_url = reverse_lazy("user_login")

    # def test_func(self):  # authenticated users can't register?
    #     return not self.request.user.is_authenticated


class UserUpdateView(
    MessagesMixin,
    UserPermissionMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = User
    form_class = RegistrationForm
    template_name = "users/update.html"

    error_message_permission = _("Sorry, you don't have permissions to update other users' data")  # noqa: E501
    error_message_login = _("You must login to be able to update your profile")  # noqa: E501
    success_message = _("User updated successfully!")

    success_url = reverse_lazy("users")
    login_url = reverse_lazy("user_login")
    redirect_url = "users"
    pk_url_kwarg = "id"


class UserDeleteView(
    MessagesDeleteProtectedMixin,
    UserPermissionMixin,
    LoginRequiredMixin,
    DeleteView
):
    model = User
    template_name = "users/delete.html"

    error_message_protected = _("User has tasks and cannot be deleted")  # noqa: E501
    error_message_permission = _("Sorry, you don't have permissions to delete other users' data")  # noqa: E501
    success_message = _("User deleted successfully!")

    success_url = reverse_lazy("users")
    login_url = reverse_lazy("user_login")
    redirect_url = "users"
    pk_url_kwarg = "id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request, _("You must login to be able to delete your profile")
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(MessagesMixin, LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm
    success_message = _("Logged in successfully!")

    # def test_func(self):  # authenticated users can't login?
    #     return not self.request.user.is_authenticated


class UserLogoutView(LogoutView):
    # def test_func(self):  # not authenticated users can't logout?
    #     return self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)


# alternative 'hard-coded' functions:

# class IndexView(ListView):
#     model = User
#     paginate_by = 10
#     template_name = 'users/index.html'
#
#     def get(self, request, *args, **kwargs):
#     users = User.objects.filter(is_superuser=False)
#     return render(request, 'users/index.html', {'users': users})


# class UserCreateView(UserPassesTestMixin, CreateView):
#
#     form_class = RegistrationForm
#     template_name = 'users/create.html'
#     success_url = reverse_lazy('user_login')
#
#     def test_func(self):  # authenticated users can't register
#         return not self.request.user.is_authenticated
#
# def get(self, request, *args, **kwargs):
#     form = RegistrationForm()
#     return render(request, 'users/create.html', {'form': form})

# def post(self, request, *args, **kwargs):
#     form = RegistrationForm(request.POST)
#     if form.is_valid():
#         form.save()
#         messages.success(request, _('User created successfully!'))
#         return redirect('user_login')
#
#     messages.warning(request, _(
#         'Something went wrong. Please check the entered data'
#     ))
#     return render(
#         request, 'users/create.html', context={
#             'form': form,
#         },
#     )


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#
#     form_class = RegistrationForm
#     model = User
#     template_name = 'users/update.html'
#     success_url = reverse_lazy('users')
#     login_url = reverse_lazy('user_login')
#     error_message = 'Sorry, you don't have permissions to update other users' data'  # noqa: E501
#     pk_url_kwarg = 'id'
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             messages.warning(request, _(
#                 'You must login to be able to update your profile'
#             ))
#             return self.handle_no_permission()
#         return super().dispatch(request, *args, **kwargs)

# def get(self, request, *args, **kwargs):
#     user_id = kwargs.get('id')
#     user = get_object_or_404(User, id=user_id)
#     form = RegistrationForm(instance=user)
#     return render(request, 'users/update.html', {
#         'form': form,
#         'user_id': user_id
#     })
#
# def post(self, request, *args, **kwargs):
#     user_id = kwargs.get('id')
#     user = get_object_or_404(User, id=user_id)
#     form = RegistrationForm(request.POST, instance=user)
#     if form.is_valid():
#         form.save()
#         messages.success(request, _('User updated successfully!'))
#         return redirect('users')
#
#     messages.warning(request, _(
#         'Something went wrong. Please check the entered data'
#     ))
#     return render(
#         request, 'users/update.html', context={
#             'form': form,
#             'user_id': user_id
#         },
#     )


# class UserDeleteView(LoginRequiredMixin, DeleteView):
#
#     model = User
#     success_url = reverse_lazy('users')
#     template_name = 'users/delete.html'
#     login_url = reverse_lazy('user_login')
#     error_message = 'Sorry, you don't have permissions to delete other users' data'  # noqa: E501
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             messages.warning(request, _(
#                 'You must login to be able to delete your profile'
#             ))
#             return self.handle_no_permission()
#         return super().dispatch(request, *args, **kwargs)

# def get(self, request, *args, **kwargs):
#     user = get_object_or_404(User, id=kwargs.get('id'))
#     if user == request.user:
#         return super().get(request, *args, **kwargs)
#     else:
#         messages.warning(request, _(
#             'Sorry, you don't have permissions to delete other users' data'  # noqa: E501
#         ))
#         return redirect('users')
#
# def post(self, request, *args, **kwargs):
#     user = get_object_or_404(User, id=kwargs.get('id'))
#     if user == request.user:
#         user.delete()
#         messages.success(request, _('User deleted successfully'))
#     else:
#         messages.warning(request, _('How did you get here?'))
#     return redirect('users')


# class UserLoginView(UserPassesTestMixin, LoginView):
#     template_name = 'users/login.html'
#     authentication_form = LoginForm
#
#     def test_func(self):  # authenticated users can't login
#         return not self.request.user.is_authenticated
#
# def get(self, request, *args, **kwargs):
#     form = (request)
#     return render(request, 'users/login.html', {'form': form})
#
# def post(self, request, *args, **kwargs):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         messages.success(request, _('User logged in successfully!'))
#         return redirect('users')
#     else:
#         messages.warning(request, _('Login data is incorrect'))
#         return redirect('users')
