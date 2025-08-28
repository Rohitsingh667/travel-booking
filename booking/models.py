from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid


class TravelOption(models.Model):
    TRAVEL_TYPES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]
    
    travel_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    available_seats = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    total_seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['departure_date', 'departure_time']

    def __str__(self):
        return f"{self.travel_id} - {self.source} to {self.destination}"

    @property
    def date(self):
        return self.departure_date
    
    @property
    def time(self):
        return self.departure_time

    def clean(self):
        if self.source and self.destination and self.source.lower() == self.destination.lower():
            raise ValidationError("Source and destination cannot be the same.")
        
        if self.departure_date and self.departure_date < timezone.now().date():
            raise ValidationError("Departure date cannot be in the past.")
        
        if self.available_seats > self.total_seats:
            raise ValidationError("Available seats cannot exceed total seats.")
        
        if self.departure_date and self.arrival_date and self.departure_date > self.arrival_date:
            raise ValidationError("Departure date cannot be after arrival date.")


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    booking_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE, related_name='bookings')
    number_of_seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    passenger_details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.booking_id} - {self.user.username}"

    @property
    def seats(self):
        return self.number_of_seats

    def clean(self):
        if self.number_of_seats and self.travel_option:
            if self.number_of_seats > self.travel_option.available_seats:
                raise ValidationError("Not enough seats available.")

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"BK{str(uuid.uuid4())[:8].upper()}"
        
        if self.travel_option and self.number_of_seats:
            self.total_price = self.travel_option.price * self.number_of_seats
        
        super().save(*args, **kwargs)

    def cancel_booking(self):
        if self.status == 'confirmed':
            self.status = 'cancelled'
            self.travel_option.available_seats += self.number_of_seats
            self.travel_option.save()
            self.save()
            return True
        return False
