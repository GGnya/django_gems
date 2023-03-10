from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from gems.forms import CreateGemForm, RegisterUserForm, LoginUserForm, UpdateUserForm, UpdateProfileForm
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


class EditGem(UpdateView):
    model = Gem
    template_name = 'gems/edit_gem.html'
    form_class = CreateGemForm
    slug_url_kwarg = 'gem_slug'

    def get_object(self, queryset=None):
        try:
            return super(EditGem, self).get_object(queryset)
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EditGem, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user == self.object.owner:
            return super(EditGem, self).post(request, *args, **kwargs)


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

    def get_context_data(self, **kwargs):
        context = super(ShowGem, self).get_context_data(**kwargs)
        user_info = User.objects.get(username=context['object'].owner)
        profile_info = Profile.objects.get(username=context['object'].owner)
        context['email'] = user_info.email
        context['phone_number'] = profile_info.phone_number
        return context


class ShowMyGems(ListView):
    model = Gem
    template_name = 'gems/index.html'
    context_object_name = 'gems'

    def get_queryset(self):
        user = self.request.user
        return Gem.objects.filter(owner=user).select_related('type')
