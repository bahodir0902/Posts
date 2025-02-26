from django.urls import path, include
from .views import *

app_name='accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('verify_code/', verify_code, name='verify_code'),
    path('create_new_password/', create_new_password, name='create_new_password')
]