from django.views.generic import FormView, View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages
from .models import CustomUser
from django.views.generic import CreateView
from django.shortcuts import redirect

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm  # This was missing
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username or password')
            return self.form_invalid(form)
class RegisterView(CreateView):
    model = CustomUser
    template_name = 'accounts/register.html'
    fields = ['username', 'email', 'password', 'phone_number']
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Registration successful. Please login.')
        return super().form_valid(form)
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect(reverse_lazy('login'))  # Redirect to login page after logout