from datetime import date
import datetime
from django.utils.timezone import now

from django.db import models
from flightbooking.apps.authentication.models import User
from flightbooking.apps.core.models import TimestampsMixin


class Flight(models.Model):
    flight_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    departure_time = models.TimeField()

    class Meta:
        ordering = ['flight_id']


class Booking(TimestampsMixin):
    booking_id = models.AutoField(primary_key=True)
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="bookings"
    )
    traveller = models.ForeignKey(
        'authentication.User',
        related_name="flights",
        on_delete=models.CASCADE)
    flight_seat = models.CharField(max_length=255)
    

    class Meta:
        ordering = ['flight_id']
    