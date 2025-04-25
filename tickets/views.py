# tickets/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from .models import Show, Booking
from accounts.models import CustomUser
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Show  # Import your Show model

class ShowListView(ListView):
    model = Show
    template_name = 'tickets/show_list.html'
    context_object_name = 'shows'
    ordering = ['-date']

class ShowDetailView(DetailView):
    model = Show
    template_name = 'tickets/show_detail.html'

class BookShowView(LoginRequiredMixin, CreateView):
    model = Booking
    fields = ['number_of_seats']
    template_name = 'tickets/book_show.html'

    def get_success_url(self):
        return reverse_lazy('tickets:show_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.show_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show'] = get_object_or_404(Show, pk=self.kwargs['pk'])
        return context

class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'tickets/booking_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

# Admin Views
class AdminShowCreateView(UserPassesTestMixin, CreateView):
    model = Show
    template_name = 'tickets/admin_show_form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_show_list')

    def test_func(self):
        return self.request.user.is_admin

class AdminShowListView(UserPassesTestMixin, ListView):
    model = Show
    template_name = 'tickets/admin_show_list.html'
    context_object_name = 'shows'

    def test_func(self):
        return self.request.user.is_admin

class AdminShowUpdateView(UserPassesTestMixin, UpdateView):
    model = Show
    template_name = 'tickets/admin_show_form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_show_list')

    def test_func(self):
        return self.request.user.is_admin

class AdminShowDeleteView(UserPassesTestMixin, DeleteView):
    model = Show
    template_name = 'tickets/admin_show_confirm_delete.html'
    success_url = reverse_lazy('admin_show_list')

    def test_func(self):
        return self.request.user.is_admin

class AdminBookingListView(UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'tickets/admin_booking_list.html'
    context_object_name = 'bookings'

    def test_func(self):
        return self.request.user.is_admin