from django.contrib import admin
from .models import TravelOption, Booking


@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ['travel_id', 'type', 'source', 'destination', 'departure_date', 'price', 'available_seats']
    list_filter = ['type', 'departure_date']
    search_fields = ['source', 'destination']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'status']
    list_filter = ['status', 'booking_date']
    search_fields = ['booking_id', 'user__username']
    readonly_fields = ['booking_id', 'total_price']
