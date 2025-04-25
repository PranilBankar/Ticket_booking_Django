# accounts/urls.py
from django.urls import path
from . import views  # Make sure to import views like this
from .views import RegisterView, LoginView, LogoutView
from accounts.views import RegisterView 
app_name = 'accounts' 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]