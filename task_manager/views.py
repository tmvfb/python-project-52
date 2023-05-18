# from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    def get(self, request, **kwargs):
        return HttpResponse('Hello, world!')
