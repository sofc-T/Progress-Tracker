from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('register', views.RegistrationView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>', views.Activation.as_view(), name='activate'),
    path('validateEmail',csrf_exempt(views.emailValidation.as_view()), name = 'validateEmail'),
    path('validatePassword', csrf_exempt(views.passwordValidation.as_view()), name = 'validatePassword'),
    path('validateUsername', csrf_exempt(views.usernameValidation.as_view()), name = 'validateUsername'),
]
