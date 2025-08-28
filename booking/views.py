from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from .models import TravelOption, Booking
from .forms import TravelSearchForm, BookingForm


def home_view(request):
    travel_options = TravelOption.objects.filter(
        departure_date__gte=timezone.now().date(),
        available_seats__gt=0
    )[:6]
    return render(request, 'booking/home.html', {'travel_options': travel_options})


def travel_options_view(request):
    form = TravelSearchForm(request.GET)
    travel_options = TravelOption.objects.filter(
        departure_date__gte=timezone.now().date(),
        available_seats__gt=0
    )
    
    if form.is_valid():
        if form.cleaned_data.get('source'):
            travel_options = travel_options.filter(source__icontains=form.cleaned_data['source'])
        if form.cleaned_data.get('destination'):
            travel_options = travel_options.filter(destination__icontains=form.cleaned_data['destination'])
        if form.cleaned_data.get('travel_type'):
            travel_options = travel_options.filter(type=form.cleaned_data['travel_type'])
        if form.cleaned_data.get('date'):
            travel_options = travel_options.filter(departure_date=form.cleaned_data['date'])
        if form.cleaned_data.get('min_price'):
            travel_options = travel_options.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data.get('max_price'):
            travel_options = travel_options.filter(price__lte=form.cleaned_data['max_price'])
    
    paginator = Paginator(travel_options, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'booking/travel_options.html', {
        'form': form,
        'page_obj': page_obj,
        'total_results': travel_options.count(),
    })


@login_required
def book_travel_view(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    
    if travel_option.available_seats <= 0:
        messages.error(request, 'No seats available')
        return redirect('travel_options')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel_option)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.travel_option = travel_option
            booking = form.save()
            messages.success(request, f'Booking confirmed! ID: {booking.booking_id}')
            return redirect('my_bookings')
    else:
        form = BookingForm(travel_option=travel_option)
    
    return render(request, 'booking/book_travel.html', {'form': form, 'travel_option': travel_option})


@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if booking.status == 'cancelled':
        messages.warning(request, 'Already cancelled')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.travel_option.available_seats += booking.number_of_seats
        booking.travel_option.save()
        booking.save()
        messages.success(request, 'Booking cancelled')
        return redirect('my_bookings')
    
    return render(request, 'booking/cancel_booking.html', {'booking': booking})


def travel_option_detail_view(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    similar_options = TravelOption.objects.filter(
        source=travel_option.source,
        destination=travel_option.destination,
        departure_date__gte=timezone.now().date(),
        available_seats__gt=0
    ).exclude(travel_id=travel_option.travel_id)[:5]
    
    return render(request, 'booking/travel_option_detail.html', {
        'travel_option': travel_option,
        'similar_options': similar_options,
    })


def ajax_cities_autocomplete(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'cities': []})
    
    cities = set()
    options = TravelOption.objects.filter(
        Q(source__icontains=query) | Q(destination__icontains=query)
    ).values_list('source', 'destination')
    
    for source, destination in options:
        if query.lower() in source.lower():
            cities.add(source)
        if query.lower() in destination.lower():
            cities.add(destination)
    
    return JsonResponse({'cities': sorted(list(cities))})
