from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import TravelOption
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Create sample travel options and users'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write('Created admin user')

        travel_options = [
            {
                'travel_id': 'FL001',
                'type': 'flight',
                'source': 'Mumbai',
                'destination': 'Delhi',
                'price': 8500.00,
                'available_seats': 50,
                'total_seats': 60
            },
            {
                'travel_id': 'TR001',
                'type': 'train',
                'source': 'Delhi',
                'destination': 'Kolkata',
                'price': 2200.00,
                'available_seats': 80,
                'total_seats': 100
            },
            {
                'travel_id': 'BUS001',
                'type': 'bus',
                'source': 'Bangalore',
                'destination': 'Chennai',
                'price': 1200.00,
                'available_seats': 40,
                'total_seats': 50
            },
            {
                'travel_id': 'FL002',
                'type': 'flight',
                'source': 'Pune',
                'destination': 'Bangalore',
                'price': 6800.00,
                'available_seats': 60,
                'total_seats': 70
            },
            {
                'travel_id': 'TR002',
                'type': 'train',
                'source': 'Ahmedabad',
                'destination': 'Mumbai',
                'price': 1800.00,
                'available_seats': 100,
                'total_seats': 120
            },
        ]

        for travel_data in travel_options:
            if not TravelOption.objects.filter(travel_id=travel_data['travel_id']).exists():
                departure_date = date.today() + timedelta(days=7)
                departure_time = time(10, 0)
                arrival_date = departure_date
                arrival_time = time(12, 0)
                
                TravelOption.objects.create(
                    travel_id=travel_data['travel_id'],
                    type=travel_data['type'],
                    source=travel_data['source'],
                    destination=travel_data['destination'],
                    departure_date=departure_date,
                    departure_time=departure_time,
                    arrival_date=arrival_date,
                    arrival_time=arrival_time,
                    price=travel_data['price'],
                    available_seats=travel_data['available_seats'],
                    total_seats=travel_data['total_seats']
                )

        self.stdout.write('Sample data created successfully!')
