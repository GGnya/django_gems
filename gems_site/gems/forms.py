from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from gems.models import Gem, Profile


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    # user_alias = forms.SlugField(label='Псевдоним', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'email', 'user_alias')


class CreateGemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = "Категория не выбрана"

    class Meta:
        model = Gem
        fields = ['title',
                  'size',
                  'type',
                  'clarity',
                  'gem_image',
                  'description',
                  'price',
                  'is_available']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 255:
            raise ValidationError('Длина превышает 255 символов')
        return title


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    user_alias = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'user_alias']
