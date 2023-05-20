# from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):

    def get(self, request, **kwargs):
        return render(request, 'base.html')
