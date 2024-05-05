from django.urls import path
from .views import home , login

urlpatterns = [
    path('', home, name='home-page'),
    path('login', login, name='login-page')
]
