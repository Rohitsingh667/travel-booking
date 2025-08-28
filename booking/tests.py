from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, time, timedelta
from .models import TravelOption, Booking
from .forms import TravelSearchForm, BookingForm


class TravelOptionModelTest(TestCase):
    """Test TravelOption model"""
    
    def setUp(self):
        self.travel_option = TravelOption.objects.create(
            travel_id='TEST001',
            type='flight',
            source='Mumbai',
            destination='Delhi',
            departure_date=date.today() + timedelta(days=7),
            departure_time=time(10, 0),
            arrival_date=date.today() + timedelta(days=7),
            arrival_time=time(12, 0),
            price=8500.00,
            available_seats=50,
            total_seats=60
        )
    
    def test_travel_option_creation(self):
        """Test travel option is created correctly"""
        self.assertEqual(self.travel_option.travel_id, 'TEST001')
        self.assertEqual(self.travel_option.type, 'flight')
        self.assertEqual(self.travel_option.source, 'Mumbai')
        self.assertEqual(self.travel_option.destination, 'Delhi')
        self.assertEqual(self.travel_option.price, 8500.00)
        self.assertEqual(self.travel_option.available_seats, 50)
    
    def test_travel_option_str_method(self):
        """Test string representation of travel option"""
        expected = "TEST001 - Mumbai to Delhi"
        self.assertEqual(str(self.travel_option), expected)
    
    def test_travel_option_properties(self):
        """Test date and time properties"""
        self.assertEqual(self.travel_option.date, self.travel_option.departure_date)
        self.assertEqual(self.travel_option.time, self.travel_option.departure_time)


class BookingModelTest(TestCase):
    """Test Booking model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.travel_option = TravelOption.objects.create(
            travel_id='TEST001',
            type='flight',
            source='Mumbai',
            destination='Delhi',
            departure_date=date.today() + timedelta(days=7),
            departure_time=time(10, 0),
            arrival_date=date.today() + timedelta(days=7),
            arrival_time=time(12, 0),
            price=8500.00,
            available_seats=50,
            total_seats=60
        )
        
        self.booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2
        )
    
    def test_booking_creation(self):
        """Test booking is created correctly"""
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.travel_option, self.travel_option)
        self.assertEqual(self.booking.number_of_seats, 2)
        self.assertEqual(self.booking.total_price, 17000.00)  # 2 * 8500
        self.assertEqual(self.booking.status, 'confirmed')
        self.assertTrue(self.booking.booking_id.startswith('BK'))
    
    def test_booking_str_method(self):
        """Test string representation of booking"""
        expected = f"{self.booking.booking_id} - testuser"
        self.assertEqual(str(self.booking), expected)
    
    def test_booking_seats_property(self):
        """Test seats property"""
        self.assertEqual(self.booking.seats, 2)
    
    def test_booking_cancel_method(self):
        """Test booking cancellation"""
        original_seats = self.travel_option.available_seats
        result = self.booking.cancel_booking()
        
        self.assertTrue(result)
        self.assertEqual(self.booking.status, 'cancelled')
        
        # Refresh travel option from database
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, original_seats + 2)


class TravelSearchFormTest(TestCase):
    """Test TravelSearchForm"""
    
    def test_valid_search_form(self):
        """Test form with valid data"""
        form_data = {
            'source': 'Mumbai',
            'destination': 'Delhi',
            'travel_type': 'flight',
            'date': date.today() + timedelta(days=7)
        }
        form = TravelSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_empty_search_form(self):
        """Test form with empty data"""
        form = TravelSearchForm(data={})
        self.assertTrue(form.is_valid())  # All fields are optional
    
    def test_date_validation(self):
        """Test date validation"""
        # Past date should be invalid
        form_data = {
            'date': date.today() - timedelta(days=1)
        }
        form = TravelSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Date cannot be in the past.', form.errors['date'])
    
    def test_same_source_destination(self):
        """Test validation for same source and destination"""
        form_data = {
            'source': 'Mumbai',
            'destination': 'mumbai'  # Same city, different case
        }
        form = TravelSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Source and destination cannot be the same.', form.non_field_errors())


class BookingFormTest(TestCase):
    """Test BookingForm"""
    
    def setUp(self):
        self.travel_option = TravelOption.objects.create(
            travel_id='TEST001',
            type='flight',
            source='Mumbai',
            destination='Delhi',
            departure_date=date.today() + timedelta(days=7),
            departure_time=time(10, 0),
            arrival_date=date.today() + timedelta(days=7),
            arrival_time=time(12, 0),
            price=8500.00,
            available_seats=5,
            total_seats=60
        )
    
    def test_valid_booking_form(self):
        """Test form with valid data"""
        form_data = {'number_of_seats': 2}
        form = BookingForm(data=form_data, travel_option=self.travel_option)
        self.assertTrue(form.is_valid())
    
    def test_seats_validation(self):
        """Test seats validation"""
        # Zero seats
        form_data = {'number_of_seats': 0}
        form = BookingForm(data=form_data, travel_option=self.travel_option)
        self.assertFalse(form.is_valid())
        
        # Too many seats
        form_data = {'number_of_seats': 15}
        form = BookingForm(data=form_data, travel_option=self.travel_option)
        self.assertFalse(form.is_valid())
        
        # More than available
        form_data = {'number_of_seats': 10}
        form = BookingForm(data=form_data, travel_option=self.travel_option)
        self.assertFalse(form.is_valid())


class BookingViewsTest(TestCase):
    """Test booking views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.travel_option = TravelOption.objects.create(
            travel_id='TEST001',
            type='flight',
            source='Mumbai',
            destination='Delhi',
            departure_date=date.today() + timedelta(days=7),
            departure_time=time(10, 0),
            arrival_date=date.today() + timedelta(days=7),
            arrival_time=time(12, 0),
            price=8500.00,
            available_seats=50,
            total_seats=60
        )
    
    def test_home_view(self):
        """Test home view"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book Your Journey')
        self.assertContains(response, self.travel_option.source)
    
    def test_travel_options_view(self):
        """Test travel options view"""
        response = self.client.get(reverse('travel_options'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search Travel Options')
        self.assertContains(response, self.travel_option.travel_id)
    
    def test_travel_options_search(self):
        """Test travel options search functionality"""
        response = self.client.get(reverse('travel_options'), {
            'source': 'Mumbai',
            'destination': 'Delhi',
            'travel_type': 'flight'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.travel_option.travel_id)
    
    def test_book_travel_view_anonymous(self):
        """Test booking view for anonymous user"""
        response = self.client.get(reverse('book_travel', args=[self.travel_option.travel_id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_book_travel_view_authenticated(self):
        """Test booking view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('book_travel', args=[self.travel_option.travel_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Complete Your Booking')
    
    def test_booking_creation(self):
        """Test creating a booking"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('book_travel', args=[self.travel_option.travel_id]), {
            'number_of_seats': 2
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful booking
        self.assertTrue(Booking.objects.filter(user=self.user).exists())
        
        booking = Booking.objects.get(user=self.user)
        self.assertEqual(booking.number_of_seats, 2)
        self.assertEqual(booking.total_price, 17000.00)
    
    def test_my_bookings_view(self):
        """Test my bookings view"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2
        )
        
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, booking.booking_id)
    
    def test_cancel_booking_view(self):
        """Test cancel booking functionality"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2
        )
        
        original_seats = self.travel_option.available_seats
        
        # Cancel the booking
        response = self.client.post(reverse('cancel_booking', args=[booking.booking_id]))
        self.assertEqual(response.status_code, 302)
        
        booking.refresh_from_db()
        self.travel_option.refresh_from_db()
        
        self.assertEqual(booking.status, 'cancelled')
        self.assertEqual(self.travel_option.available_seats, original_seats + 2)


class AccountViewsTest(TestCase):
    """Test account views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_signup_view(self):
        """Test signup view"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
    
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_view(self):
        """Test login view"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome Back')
    
    def test_profile_view(self):
        """Test profile view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Profile')
        self.assertContains(response, self.user.username)
    
    def test_edit_profile_view(self):
        """Test edit profile view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')
    
    def test_profile_update(self):
        """Test profile update"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone_number': '+91 9876543210'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
