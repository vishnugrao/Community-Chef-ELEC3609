from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_homepage_view(self):
        # Test the 'homepage' view
        response = self.client.get(reverse('profile_manager:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_user_logout_view(self):
        # Authenticate the user
        client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Test the 'user_logout' view for an authenticated user
        response = client.get(reverse("profile_manager:logout"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_incorrect_user_view(self):
        # Test the 'incorrect_user' view
        response = self.client.get(reverse('profile_manager:incorrect_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incorrect_user.html')
