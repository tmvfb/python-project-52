# from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')
