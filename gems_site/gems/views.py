from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from django.db import transaction
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from gems.forms import CreateGemForm
from gems.models import Gem


class GemsHome(ListView):
    model = Gem
    template_name = 'gems/index.html'
    context_object_name = 'gems'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     c_def = self.get_user_context(title='Main page')
    #     # user_menu = menu.copy()
    #     # if not self.request.user.is_authenticated:
    #     #     user_menu.pop(1)
    #     #
    #     # context['menu'] = user_menu
    #     return {**context, **c_def}

    def get_queryset(self):
        return Gem.objects.filter(is_available=True).select_related('type')


class CreateGem(CreateView):
    form_class = CreateGemForm
    template_name = 'gems/create_gem.html'
    success_url = reverse_lazy('home')
    # login_url = reverse_lazy('')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title='Добавление статьи')
    #     return {**context, **c_def}