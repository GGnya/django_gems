from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from gems.forms import CreateGemForm, RegisterUserForm, LoginUserForm, ProfileForm, UpdateUserForm, UpdateProfileForm
from gems.models import Gem, Profile


class GemsHome(ListView):
    model = Gem
    template_name = 'gems/index.html'
    context_object_name = 'gems'


    def get_queryset(self):
        return Gem.objects.filter(is_available=True).select_related('type')


class CreateGem(CreateView):
    form_class = CreateGemForm
    template_name = 'gems/create_gem.html'
    success_url = reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'gems/register.html'
    success_url = reverse_lazy('login')


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'gems/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class ShowProfilePageView(ListView):
    model = Profile
    template_name = 'gems/profile.html'


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'gems/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})



class Basket(CreateView):
    pass
    # form_class = BasketForm
    # template_name = 'gems/basket.html'

def logout_user(request):
    logout(request)
    return redirect('login')
