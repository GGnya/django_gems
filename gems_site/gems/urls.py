from django.urls import path

# from gems.views import logout_user, LoginUser, RegisterUser
from gems.views import GemsHome, CreateGem, RegisterUser, LoginUser, Basket, Profile

urlpatterns = [
    path('', GemsHome.as_view(), name='home'),
    path('create_gem/', CreateGem.as_view(), name='create_gem'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', Profile.as_view(), name='profile'),
    path('basket/', Basket.as_view(), name='basket'),

    # path('login/', LoginUser.as_view(), name='login'),
    # path('logout/', logout_user, name='logout'),
    # path('register/', RegisterUser.as_view(), name='register'),
]
