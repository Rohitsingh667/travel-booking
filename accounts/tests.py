from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from .models import UserProfile
from .forms import CustomUserCreationForm, UserProfileForm


class UserProfileModelTest(TestCase):
    """Test UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_profile_creation(self):
        """Test that user profile is created automatically"""
        # Profile should be created automatically via signal
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_user_profile_str_method(self):
        """Test string representation of user profile"""
        expected = "testuser's Profile"
        self.assertEqual(str(self.user.profile), expected)
    
    def test_user_profile_fields(self):
        """Test user profile fields"""
        profile = self.user.profile
        profile.phone_number = '+91 9876543210'
        profile.date_of_birth = date(1990, 1, 1)
        profile.address = 'Test Address, Mumbai, India'
        profile.save()
        
        self.assertEqual(profile.phone_number, '+91 9876543210')
        self.assertEqual(profile.date_of_birth, date(1990, 1, 1))
        self.assertEqual(profile.address, 'Test Address, Mumbai, India')


class CustomUserCreationFormTest(TestCase):
    """Test CustomUserCreationForm"""
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_required_fields(self):
        """Test required fields validation"""
        form_data = {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
    
    def test_password_mismatch(self):
        """Test password mismatch validation"""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_duplicate_username(self):
        """Test duplicate username validation"""
        # Create a user first
        User.objects.create_user(username='existinguser', email='existing@example.com')
        
        form_data = {
            'username': 'existinguser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_form_save(self):
        """Test form save method"""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'newuser@example.com')


class UserProfileFormTest(TestCase):
    """Test UserProfileForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone_number': '+91 9876543210',
            'date_of_birth': '1990-01-01',
            'address': 'Updated Address, Mumbai, India'
        }
        form = UserProfileForm(data=form_data, instance=self.user.profile, user=self.user)
        self.assertTrue(form.is_valid())
    
    def test_form_initialization(self):
        """Test form initialization with user data"""
        form = UserProfileForm(instance=self.user.profile, user=self.user)
        self.assertEqual(form.fields['first_name'].initial, self.user.first_name)
        self.assertEqual(form.fields['last_name'].initial, self.user.last_name)
        self.assertEqual(form.fields['email'].initial, self.user.email)
    
    def test_form_save(self):
        """Test form save method"""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone_number': '+91 9876543210',
            'date_of_birth': '1990-01-01',
            'address': 'Updated Address, Mumbai, India'
        }
        form = UserProfileForm(data=form_data, instance=self.user.profile, user=self.user)
        self.assertTrue(form.is_valid())
        
        profile = form.save()
        
        # Refresh user from database
        self.user.refresh_from_db()
        
        # Check user fields are updated
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        
        # Check profile fields are updated
        self.assertEqual(profile.phone_number, '+91 9876543210')
        self.assertEqual(profile.date_of_birth, date(1990, 1, 1))
        self.assertEqual(profile.address, 'Updated Address, Mumbai, India')


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
    
    def test_signup_view_get(self):
        """Test signup view GET request"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
        self.assertContains(response, 'form')
    
    def test_signup_view_post_valid(self):
        """Test signup view POST request with valid data"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        # User should be created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # User profile should be created automatically
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'profile'))
    
    def test_signup_view_post_invalid(self):
        """Test signup view POST request with invalid data"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'weak',
            'password2': 'different'
        })
        
        # Should return to form with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        
        # User should not be created
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Profile')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.first_name)
    
    def test_profile_view_anonymous(self):
        """Test profile view for anonymous user"""
        response = self.client.get(reverse('profile'))
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")
    
    def test_edit_profile_view_get(self):
        """Test edit profile view GET request"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')
        self.assertContains(response, 'form')
    
    def test_edit_profile_view_post_valid(self):
        """Test edit profile view POST request with valid data"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone_number': '+91 9876543210',
            'date_of_birth': '1990-01-01',
            'address': 'Updated Address, Mumbai, India'
        })
        
        # Should redirect to profile page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        
        # User and profile should be updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.phone_number, '+91 9876543210')
    
    def test_edit_profile_view_anonymous(self):
        """Test edit profile view for anonymous user"""
        response = self.client.get(reverse('edit_profile'))
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('edit_profile')}")


class AuthenticationTest(TestCase):
    """Test authentication functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Should redirect to home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
        # User should be logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        # Should return to login form with error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_logout(self):
        """Test logout functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        
        # Should redirect to home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
    
    def test_login_redirect(self):
        """Test login redirect functionality"""
        # Try to access profile page without login
        response = self.client.get(reverse('profile'))
        
        # Should redirect to login with next parameter
        self.assertEqual(response.status_code, 302)
        expected_url = f"{reverse('login')}?next={reverse('profile')}"
        self.assertRedirects(response, expected_url)
        
        # Login and check redirect
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        }, HTTP_REFERER=expected_url)
        
        # Should redirect to originally requested page
        self.assertEqual(response.status_code, 302)
