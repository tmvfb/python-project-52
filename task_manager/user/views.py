from django.shortcuts import render
from django.views import View


# Create your views here.
class IndexView(View):

	def get(self, request, *args, **kwargs):
		users = User.objects.all()
		return render(request, 'user/index.html', {
			'users': users
		})


class UserCreateView(View):

	def get(self, request, *args, **kwargs):
		pass

	def post(self, request, *args, **kwargs):
		pass


class UserUpdateView(View):

	def get(self, request, *args, **kwargs):
		pass

	def post(self, request, *args, **kwargs):
		pass


class UserDeleteView(View):

	def get(self, request, *args, **kwargs):
		pass

	def post(self, request, *args, **kwargs):
		pass


class UserLoginView(View):

	def get(self, request, *args, **kwargs):
		pass

	def post(self, request, *args, **kwargs):
		pass


class UserLogoutView(View):

	def post(self, request, *args, **kwargs):
		pass
