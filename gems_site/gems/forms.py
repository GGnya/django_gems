from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from phonenumber_field.widgets import PhoneNumberPrefixWidget

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
        fields = ('username', 'user_alias')


class CreateGemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = "Тип не выбран"

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
        # exclude = ['date_created', 'date_updated', 'owner']

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

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    user_alias = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_number = PhoneNumberField(region='RU', widget=PhoneNumberPrefixWidget)

    class Meta:
        model = Profile
        fields = ['user_alias', 'phone_number']
