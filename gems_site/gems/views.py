from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView, UpdateView

from gems.forms import CreateGemForm, RegisterUserForm, LoginUserForm, ProfileForm, UpdateUserForm, UpdateProfileForm
from gems.models import Gem, Profile


class GemsHome(ListView):
    model = Gem
    template_name = 'gems/index.html'
    context_object_name = 'gems'

    def get_queryset(self):
        # print(Gem.objects.filter(owner__isnull=False).select_related('type'))
        return Gem.objects.filter(is_available=True).select_related('type')


class CreateGem(CreateView):
    form_class = CreateGemForm
    template_name = 'gems/create_gem.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = CreateGemForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                gem = form.save(commit=False)
                gem.owner_id = request.user.pk
                gem.save()
                return redirect('home')
        return render(request, 'gems/create_gem.html', locals())


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


# class UpdateProfile(UpdateView):
#     model = Profile
#     form_class = UpdateUserForm
#     second_form_class = UpdateProfileForm
#     template_name = 'gems/update_profile.html'
#
#     def get_context_data(self, **kwargs):
#         # context = super(UpdateProfile, self).get_context_data(**kwargs)
#         # # print(context)
#         #
#         # if 'form' not in context:
#         #     kwargs['form'] = self.form_class(instance=self.get_object())
#         #
#         # if 'form2' not in context:
#         #     # context = self.second_form_class()
#         #     self.second_form_class(instance=self.get_object().username)
#         #     # context['form2'] = self.second_form_class()
#         # return context
#
#         context = super(UpdateProfile, self).get_context_data(**kwargs)
#         print(context)
#         if 'form' not in context:
#             # print(self.request.GET.user.pk)
#             context['form'] = self.form_class(self.request.GET)
#         if 'form2' not in context:
#             # print(self.second_form_class(self.request.GET))
#             context['form2'] = self.second_form_class(self.request.GET)
#
#         return context
#
#     def form_invalid(self, **kwargs):
#         return self.render_to_response(self.get_context_data(**kwargs))
#
#     def get_object(self, query_set=None):
#         # print(get_object_or_404(User, pk=self.request.session['_auth_user_id']))
#         # print(get_object_or_404(Profile, username=self.request.session['_auth_user_id']))
#         return get_object_or_404(User, pk=self.request.session['_auth_user_id'])
#
#     def get(self, request, *args, **kwargs):
#         super(UpdateProfile, self).get(request, *args, **kwargs)
#
#         form = self.form_class
#         form2 = self.second_form_class
#         # print(self.get_object())
#         return self.render_to_response(self.get_context_data(
#             object=self.object, form=form, form2=form2))
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#
#         form = self.form_class(request.POST)
#         form2 = self.second_form_class(request.POST)
#         if form.is_valid() and form2.is_valid():
#             userdata = form.save(commit=False)
#             userdata.save()
#             profileedata = form2.save(commit=False)
#             profileedata.user = userdata
#             profileedata.save()
#             messages.success(self.request, 'Settings saved successfully')
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.render_to_response(
#                 self.get_context_data(form=form, form2=form2))
#         if 'form' in request.POST:
#             form_class = self.form_class
#             form_name = 'form'
#         if 'form2' in request.POST:
#         # else:
#             form_class = self.second_form_class
#             form_name = 'form2'
#
#         form = self.get_form(form_class)
#         print(form)
#
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(**{form_name: form})


class UpdateProfile(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    second_form_class = UpdateUserForm
    template_name = 'gems/update_profile.html'

    def get(self, *args, **kwargs):
        user_form = UpdateUserForm(instance=self.request.user)
        profile_form = UpdateProfileForm(instance=self.request.user.profile)
        return render(self.request, 'gems/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})
    def post(self, request, *args, **kwargs):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')



class Basket(CreateView):
    pass
    # form_class = BasketForm
    # template_name = 'gems/basket.html'


def logout_user(request):
    logout(request)
    return redirect('login')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'gems/change_password.html', {
        'form': form
    })


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'gems/password_reset.html'
    email_template_name = 'gems/password_email_reset.html'
    subject_template_name = 'gems/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ShowGem(DetailView):
    model = Gem
    template_name = 'gems/gem.html'
    slug_url_kwarg = 'gem_slug'
    context_object_name = 'gem'


class ShowMyGems(ListView):
    model = Gem
    template_name = 'gems/index.html'
    context_object_name = 'gems'

    def get_queryset(self):
        # print(Gem.objects.filter(owner__isnull=False).select_related('type'))
        user = self.request.user
        return Gem.objects.filter(owner=user).select_related('type')
