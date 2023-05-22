from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_superuser=False)
        print(users)
        return render(request, "users/index.html", {"users": users})


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, "users/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("User created successfully!"))
            return redirect("users")

        messages.warning(request, _(
            "Something went wrong. Please check the entered data"
        ))
        return render(
            request, "users/create.html", context={
                "form": form,
            },
        )


class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = RegistrationForm(instance=user)
        return render(request, "users/update.html", {
            "form": form,
            "user_id": user_id
        })

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = RegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _("User updated successfully!"))
            return redirect("users")

        messages.warning(request, _(
            "Something went wrong. Please check the entered data"
        ))
        return render(
            request, "users/update.html", context={
                "form": form,
                "user_id": user_id
            },
        )


class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        return render(request, "users/delete.html", context={
            "user": user
        })

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
            messages.success(request, _(
                "User deleted successfully"
            ))
        else:
            messages.warning(request, _(
                "How did you get here? This user does not exist."
            ))
        return redirect('users')


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm
    # def get(self, request, *args, **kwargs):
    #     form = (request)
    #     return render(request, "users/login.html", {"form": form})
    #
    # def post(self, request, *args, **kwargs):
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         messages.success(request, _("User logged in successfully!"))
    #         return redirect("users")
    #     else:
    #         messages.warning(request, _("Login data is incorrect"))
    #         return redirect("users")


class UserLogoutView(LogoutView):
    pass
