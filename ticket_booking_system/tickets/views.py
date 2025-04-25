from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, 
    UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Show, Booking

# User Views
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show'] = get_object_or_404(Show, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.show = get_object_or_404(Show, pk=self.kwargs['pk'])
        messages.success(self.request, 'Booking successful!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tickets:booking_history')

class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'tickets/booking_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

# Admin Views
class AdminShowListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Show
    template_name = 'tickets/admin_show_list.html'
    context_object_name = 'shows'

    def test_func(self):
        return self.request.user.is_admin

class AdminShowCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Show
    fields = '__all__'
    template_name = 'tickets/admin_show_form.html'
    success_url = reverse_lazy('tickets:admin_show_list')

    def test_func(self):
        return self.request.user.is_admin

class AdminShowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Show
    fields = '__all__'
    template_name = 'tickets/admin_show_form.html'
    success_url = reverse_lazy('tickets:admin_show_list')

    def test_func(self):
        return self.request.user.is_admin

class AdminShowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Show
    template_name = 'tickets/admin_show_confirm_delete.html'
    success_url = reverse_lazy('tickets:admin_show_list')

    def test_func(self):
        return self.request.user.is_admin

class AdminBookingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'tickets/admin_booking_list.html'
    context_object_name = 'bookings'

    def test_func(self):
        return self.request.user.is_admin