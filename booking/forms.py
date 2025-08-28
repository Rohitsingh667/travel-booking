from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking


class TravelSearchForm(forms.Form):
    TRAVEL_TYPES = [('', 'All'), ('flight', 'Flight'), ('train', 'Train'), ('bus', 'Bus')]
    
    source = forms.CharField(max_length=100, required=False)
    destination = forms.CharField(max_length=100, required=False)
    travel_type = forms.ChoiceField(choices=TRAVEL_TYPES, required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    min_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise ValidationError("Date cannot be in the past.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        destination = cleaned_data.get('destination')
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if source and destination and source.lower() == destination.lower():
            raise ValidationError("Source and destination cannot be the same.")
        
        if min_price and max_price and min_price > max_price:
            raise ValidationError("Min price cannot be greater than max price.")
        
        return cleaned_data


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']

    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        super().__init__(*args, **kwargs)

    def clean_number_of_seats(self):
        seats = self.cleaned_data['number_of_seats']
        
        if seats <= 0:
            raise ValidationError("Must book at least 1 seat.")
        
        if seats > 10:
            raise ValidationError("Cannot book more than 10 seats.")
        
        if self.travel_option and seats > self.travel_option.available_seats:
            raise ValidationError(f'Only {self.travel_option.available_seats} seats available.')
        
        return seats

    def save(self, commit=True):
        booking = super().save(commit=False)
        if commit:
            booking.save()
            self.travel_option.available_seats -= booking.number_of_seats
            self.travel_option.save()
        return booking
