from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm
from django.utils.translation import gettext as _
from django.http import HttpResponse


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
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
            request,
            "users/create.html",
            {
                "form": form,
            },
        )


class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Not yet implemented!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Not yet implemented!')


class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Not yet implemented!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Not yet implemented!')


class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Not yet implemented!')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Not yet implemented!')


class UserLogoutView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse('Not yet implemented!')
