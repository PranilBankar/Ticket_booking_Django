# booking_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', RedirectView.as_view(url='shows/'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('shows/', include('tickets.urls',namespace='tickets')),
]