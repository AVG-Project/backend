# from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect


# from django.contrib import messages
# from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.generic import ListView, DetailView, CreateView, UpdateView
# from django_filters.views import FilterView
#
# from Istok_app.filters import FinishedFurnitureFilter
# from .models import Finished_furniture, Application, Orders, Parts
# from .forms import Finished_furnitureCreateForm, ApplicationCreateForm, OrdersCreateForm, PartsCreateForm


def home(request):
    return render(request, 'Istok_app/home.html')


def about(request):
    return render(request, 'Istok_app/about.html')
