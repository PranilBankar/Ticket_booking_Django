# tickets/models.py

from django.db import models
from accounts.models import CustomUser

class Show(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    duration = models.DurationField()
    venue = models.CharField(max_length=200)
    total_seats = models.PositiveIntegerField()
    price_per_seat = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"

    def available_seats(self):
        booked_seats = self.booking_set.aggregate(models.Sum('number_of_seats'))['number_of_seats__sum'] or 0
        return self.total_seats - booked_seats

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.show.title} - {self.number_of_seats} seats"

    def total_price(self):
        return self.number_of_seats * self.show.price_per_seat