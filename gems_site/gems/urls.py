from django.urls import path
from django.contrib.auth import views as auth_views

from gems.views import GemsHome, CreateGem, RegisterUser, LoginUser, ShowProfilePageView, \
    logout_user, change_password, ResetPasswordView, ShowGem, ShowMyGems, UpdateProfile, EditGem

urlpatterns = [
    path('', GemsHome.as_view(), name='home'),
    path('create_gem/', CreateGem.as_view(), name='create_gem'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', ShowProfilePageView.as_view(), name='profile'),
    path('update_profile/', UpdateProfile.as_view(), name='update_profile'),
    path('logout/', logout_user, name='logout'),
    path('update_profile/change_password/', change_password, name='change_password'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='gems/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='gems/password_reset_complete.html'),
         name='password_reset_complete'),
    path('gem/<slug:gem_slug>/', ShowGem.as_view(), name='gem'),
    path('my_gems', ShowMyGems.as_view(), name='mygems'),
    path('gem/edit_gem/<slug:gem_slug>/', EditGem.as_view(), name='edit_gem')

]
