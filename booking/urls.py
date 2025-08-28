from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('travel-options/', views.travel_options_view, name='travel_options'),
    path('travel-options/<str:travel_id>/', views.travel_option_detail_view, name='travel_option_detail'),
    path('book/<str:travel_id>/', views.book_travel_view, name='book_travel'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('cancel-booking/<str:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('ajax/cities/', views.ajax_cities_autocomplete, name='ajax_cities'),
]
