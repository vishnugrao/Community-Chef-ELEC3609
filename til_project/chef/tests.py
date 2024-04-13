from django.urls import reverse
from django.contrib.auth.models import User
from .models import Availability, Chef, Ingredient, Recipe
from django.test import TestCase, Client
from django.core.exceptions import ValidationError


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user for Chef model
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        
        # Create a Chef
        self.chef = Chef.objects.create(auth_user=self.user, firstname='John', lastname='Doe', username='johndoe', email='johndoe@example.com', password='chefpassword')
        
        # Create Ingredients
        self.ingredient1 = Ingredient.objects.create(name='Salt', price=2.50)
        self.ingredient2 = Ingredient.objects.create(name='Pepper', price=3.00)
        
        # Create Availability
        self.availability = Availability.objects.create(chef=self.chef, date='2023-12-25', start_time='09:00:00', end_time='12:00:00', vacancies=10, filled_seats=5, additional_info='Holiday special')
        
        # Create Recipe
        self.recipe = Recipe.objects.create(chef=self.chef, name='Test Recipe', description='A test recipe', claps=0, total_price=0)
        self.recipe.ingredients.add(self.ingredient1, self.ingredient2)
    
    def test_chef_model(self):
        self.assertEqual(self.chef.firstname, 'John')
        self.assertEqual(self.chef.lastname, 'Doe')
        self.assertEqual(self.chef.username, 'johndoe')
        self.assertEqual(self.chef.email, 'johndoe@example.com')
        self.assertEqual(self.chef.password, 'chefpassword')
    
    def test_availability_model(self):
        self.assertEqual(self.availability.chef, self.chef)
        self.assertEqual(self.availability.date, '2023-12-25')
        self.assertEqual(self.availability.start_time, '09:00:00')
        self.assertEqual(self.availability.end_time, '12:00:00')
        self.assertEqual(self.availability.vacancies, 10)
        self.assertEqual(self.availability.filled_seats, 5)
        self.assertEqual(self.availability.additional_info, 'Holiday special')
    
    def test_recipe_model(self):
        self.assertEqual(self.recipe.chef, self.chef)
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.description, 'A test recipe')
        self.assertEqual(self.recipe.claps, 0)
        self.assertEqual(self.recipe.total_price, 0)
        self.assertEqual(self.recipe.ingredients.count(), 2)  # Check if ingredients are added

    def test_ingredient_model(self):
        self.assertEqual(self.ingredient1.name, 'Salt')
        self.assertEqual(self.ingredient1.price, 2.50)
        self.assertEqual(self.ingredient2.name, 'Pepper')
        self.assertEqual(self.ingredient2.price, 3.00)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.chef = Chef.objects.create(auth_user=self.user, firstname='John', lastname='Doe', username='johndoe', email='johndoe@example.com', password='chefpassword')
        self.recipe = Recipe.objects.create(name='Test Recipe', description='A test recipe', chef=self.chef, total_price=0)
        # Create any other necessary objects or instances
    
    def test_chef_login_view(self):
        client = Client()

        # Test successful login
        response = client.post(reverse('chef:chef_login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  # Check if the login stays
        
        # Test invalid login
        response = client.post(reverse('chef:chef_login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)  # Check if login fails and page stays the same
        
    def test_create_chef_profile_view(self):
        client = Client()

        # Test successful profile creation
        response = client.post(reverse('chef:create_chef_profile'), {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 200)  # Check if the profile creation stays
        
        # Test invalid profile creation
        response = client.post(reverse('chef:create_chef_profile'), {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  # Check if creation fails and page stays the same
        

    def test_chef_home_view(self):
        client = Client()

        # Test authenticated user access
        client.force_login(self.chef.auth_user)
        response = client.get(reverse('chef:chef_home', args=[self.chef.id]))
        self.assertEqual(response.status_code, 200)  # Check if the logged-in user accesses their home
        

    def test_add_recipe_view(self):
        client = Client()

        # Test authenticated user adding a recipe
        client.force_login(self.chef.auth_user)
        response = client.post(reverse('chef:add_recipe', args=[self.chef.id]), {'name': 'New Recipe', 'description': 'New description'})
        self.assertEqual(response.status_code, 200)  # Check if the recipe is added
        

    def test_chef_profile_view(self):
        client = Client()

        # Test authenticated user access
        client.force_login(self.chef.auth_user)
        response = client.get(reverse('chef:chef_profile', args=[self.chef.id]))
        self.assertEqual(response.status_code, 200)  # Check if the authenticated user accesses their profile
        
        

    def test_display_recipes_view(self):
        client = Client()

        # Test authenticated user access
        client.force_login(self.chef.auth_user)
        response = client.get(reverse('chef:display_recipes', args=[self.chef.id]))
        self.assertEqual(response.status_code, 200)  # Check if the authenticated user accesses their recipes
        

    def test_recipe_profile_view(self):
        client = Client()

        # Test existing recipe profile
        response = client.get(reverse('chef:recipe_profile', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)  # Check if the recipe profile is accessible
        
        # Test non-existent recipe profile
        response = client.get(reverse('chef:recipe_profile', args=[100]))  # Assuming 100 is an invalid recipe ID
        self.assertEqual(response.status_code, 404)  # Check if the page shows a 404 error for a non-existent recipe
        
    def test_update_profile_view(self):
        client = Client()

        # Test authenticated user updating profile
        client.force_login(self.chef.auth_user)
        response = client.post(reverse('chef:update_profile', args=[self.chef.id]), {'username': 'updatedusername', 'firstname': 'updatedfirstname', 'lastname':'Doe', 'email':'johndoe@example.com', 'password':'chefpassword'})
        self.assertEqual(response.status_code, 302)  # Check if the profile is updated
        
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Availability, Chef
from .AvailabilityForm import AvailabilityForm

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Availability, Chef
from .AvailabilityForm import AvailabilityForm

class BookingViewsTestCase(TestCase):
    def setUp(self):
        # Create a user and chef for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.chef = Chef.objects.create(username='testchef', auth_user=self.user)

    def test_chef_availability_view(self):
        response = self.client.get(reverse('chef:chef_availability', args=[self.chef.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_chef_availabilities_view(self):
        response = self.client.get(reverse('chef:get_chef_availabilities', args=[self.chef.id]))
        self.assertEqual(response.status_code, 200)

class BookingModelsTestCase(TestCase):
    def setUp(self):
        # Create a user and chef for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.chef = Chef.objects.create(username='testchef', auth_user=self.user)

    def test_availability_model(self):
        availability = Availability(
            chef=self.chef,
            date='2023-11-15',
            start_time='09:00:00',
            end_time='12:00:00',
            vacancies=10,
            filled_seats=0,
            additional_info='Available for bookings'
        )
        availability.save()

        self.assertEqual(availability.chef, self.chef)
        self.assertEqual(availability.date, '2023-11-15')
        self.assertEqual(availability.start_time, '09:00:00')
        self.assertEqual(availability.end_time, '12:00:00')
        self.assertEqual(availability.vacancies, 10)
        self.assertEqual(availability.filled_seats, 0)
        self.assertEqual(availability.additional_info, 'Available for bookings')

    # def test_availability_model_edge_cases(self):
        # Test the availability model with edge cases

        # # Create an availability object with negative vacancies
        # availability1 = Availability(
        #     chef=self.chef,
        #     date='2023-11-15',
        #     start_time='09:00:00',
        #     end_time='12:00:00',
        #     vacancies=-1,
        #     filled_seats=0,
        #     additional_info='Invalid vacancies'
        # )
        # with self.assertRaises(ValueError):
        #     availability1.full_clean()  

        # Create an availability object with filled seats greater than vacancies
        # availability2 = Availability(
        #     chef=self.chef,
        #     date='2023-11-15',
        #     start_time='09:00:00',
        #     end_time='12:00:00',
        #     vacancies=10,
        #     filled_seats=15,
        #     additional_info='Invalid filled seats'
        # )
        # with self.assertRaises(ValueError):
        #     availability2.full_clean()  

        # # Create an availability object with end time before start time
        # availability3 = Availability(
        #     chef=self.chef,
        #     date='2023-11-15',
        #     start_time='14:00:00',
        #     end_time='12:00:00',
        #     vacancies=10,
        #     filled_seats=5,
        #     additional_info='Invalid time range'
        # )
        # with self.assertRaises(ValueError):
        #     availability3.full_clean()

        # # Create an availability object with a long additional_info
        # long_info = 'A' * 1000  # Create a long string
        # # Not yet implemented!!
        # availability4 = Availability(
        #     chef=self.chef,
        #     date='2023-11-15',
        #     start_time='09:00:00',
        #     end_time='12:00:00',
        #     vacancies=10,
        #     filled_seats=5,
        #     additional_info=long_info
        # )
        # with self.assertRaises(ValueError):
        #     availability4.full_clean()

    def test_availability_form_validity(self):
        # Test the validity of the AvailabilityForm

        # Create a valid form
        valid_form_data = {
            'date': '2023-11-15',
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'vacancies': 10,
            'filled_seats': 0,
            'additional_info': 'Available for bookings'
        }
        valid_form = AvailabilityForm(data=valid_form_data)
        self.assertTrue(valid_form.is_valid())

        # # Create a form with negative vacancies
        # invalid_form_data = {
        #     'date': '2023-11-15',
        #     'start_time': '09:00:00',
        #     'end_time': '12:00:00',
        #     'vacancies': -1,
        #     'filled_seats': 0,
        #     'additional_info': 'Invalid vacancies'
        # }
        # invalid_form = AvailabilityForm(data=invalid_form_data)
        # self.assertFalse(invalid_form.is_valid())

        # # Create a form with filled seats greater than vacancies
        # invalid_form_data = {
        #     'date': '2023-11-15',
        #     'start_time': '09:00:00',
        #     'end_time': '12:00:00',
        #     'vacancies': 10,
        #     'filled_seats': 15,
        #     'additional_info': 'Invalid filled seats'
        # }
        # invalid_form = AvailabilityForm(data=invalid_form_data)
        # self.assertFalse(invalid_form.is_valid())

class ChefAvailabilityTestCase(TestCase):
    def setUp(self):
        # Create a user and chef for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.chef = Chef.objects.create(username='testchef', auth_user=self.user)

    def test_chef_availability_view(self):
        response = self.client.get(reverse('chef:chef_availability', args=[self.chef.id]))
        self.assertEqual(response.status_code, 200)

    def test_chef_availability_post_valid_form(self):
        data = {
            'date': '2023-11-15',
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'vacancies': 10,
            'filled_seats': 0,
            'additional_info': 'Available for bookings'
        }

        response = self.client.post(reverse('chef:chef_availability', args=[self.chef.id]), data)
        self.assertEqual(response.status_code, 200)

    def test_chef_availability_post_invalid_form(self):
        data = {
            'date': '2023-11-15',
            'start_time': '12:00:00',  # Invalid: End time should be after start time
            'end_time': '09:00:00',
            'vacancies': -1,  # Invalid: Vacancies cannot be negative
            'filled_seats': 5,
            'additional_info': 'Invalid form'
        }
        with self.assertRaisesMessage(ValidationError, 'Start time must be before end time'):
            response = self.client.post(reverse('chef:chef_availability', args=[self.chef.id]), data)
            self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Start time must be before end time')
        # self.assertContains(response, 'Vacancies cannot be negative')

    def test_chef_availability_post_overlapping_availability(self):
        availability = Availability.objects.create(
            chef=self.chef,
            date='2023-11-15',
            start_time='09:00:00',
            end_time='12:00:00',
            vacancies=10,
            filled_seats=0,
            additional_info='Available for bookings'
        )

        data = {
            'date': '2023-11-15',
            'start_time': '10:00:00',  # Overlapping with the existing availability
            'end_time': '11:00:00',  # Overlapping with the existing availability
            'vacancies': 5,
            'filled_seats': 0,
            'additional_info': 'Overlapping form'
        }
        with self.assertRaisesMessage(ValidationError, 'Availability overlaps with an existing booking'):
            response = self.client.post(reverse('chef:chef_availability', args=[self.chef.id]), data)
            self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Availability overlaps with an existing booking')

    def test_chef_availability_post_max_vacancies(self):
        data = {
            'date': '2023-11-15',
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'vacancies': 101,  # Exceeds the maximum limit
            'filled_seats': 0,
            'additional_info': 'Exceeding max vacancies'
        }
        with self.assertRaisesMessage(ValidationError, 'Vacancies exceed the maximum limit'):
            response = self.client.post(reverse('chef:chef_availability', args=[self.chef.id]), data)
            self.assertEqual(response.status_code, 200)

    def test_chef_availability_post_existing_availability(self):
        availability = Availability.objects.create(
            chef=self.chef,
            date='2023-11-15',
            start_time='09:00:00',
            end_time='12:00:00',
            vacancies=10,
            filled_seats=0,
            additional_info='Available for bookings'
        )

        data = {
            'date': '2023-11-15',
            'start_time': '09:00:00',
            'end_time': '12:00:00',
            'vacancies': 5,
            'filled_seats': 0,
            'additional_info': 'Existing availability'
        }
        with self.assertRaisesMessage(ValidationError, 'Availability overlaps with an existing booking'):
            response = self.client.post(reverse('chef:chef_availability', args=[self.chef.id]), data)
            self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Availability already exists')
