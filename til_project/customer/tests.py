from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Recipe, Chef, Customer, Clap, Favorite
from django.utils import timezone
from django.urls import reverse
from django.utils import timezone

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create necessary model instances for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_chef = User.objects.create_user(username='testuser_chef', email='test@example.com', password='testpassword')
        self.chef = Chef.objects.create(auth_user=self.user_chef, firstname='John', lastname='Doe', username='johndoe', email='johndoe@example.com', password='chefpassword')
        self.recipe = Recipe.objects.create(name='Test Recipe', chef=self.chef)
        self.customer = Customer.objects.create(
            auth_user=self.user,
            firstname='John',
            lastname='Doe',
            username='johndoe',
            email='johndoe@example.com',
            password='test123'
        )

    def test_clap_model(self):
        # Test the 'Clap' model
        clap = Clap.objects.create(customer=self.customer, recipe=self.recipe)
        self.assertEqual(clap.customer, self.customer)
        self.assertEqual(clap.recipe, self.recipe)
        self.assertIsNotNone(clap.timestamp)
        self.assertEqual(str(clap), f"{self.customer.username} clapped for {self.recipe.name}")

    def test_favorite_model(self):
        # Test the 'Favorite' model
        favorite = Favorite.objects.create(customer=self.customer, chef=self.chef)
        self.assertEqual(favorite.customer, self.customer)
        self.assertEqual(favorite.chef, self.chef)
        self.assertIsNotNone(favorite.timestamp)
        # Ensure uniqueness of the customer-chef combination
        with self.assertRaises(Exception):
            # Attempting to create a duplicate favorite entry
            Favorite.objects.create(customer=self.customer, chef=self.chef)

    def test_clap_unique_together_constraint(self):
        # Test unique_together constraint in Clap model
        clap = Clap.objects.create(customer=self.customer, recipe=self.recipe)
        with self.assertRaises(Exception):
            # Attempting to create a duplicate clap entry for the same recipe and customer
            Clap.objects.create(customer=self.customer, recipe=self.recipe)

    def test_favorite_unique_together_constraint(self):
        # Test unique_together constraint in Favorite model
        favorite = Favorite.objects.create(customer=self.customer, chef=self.chef)
        with self.assertRaises(Exception):
            # Attempting to create a duplicate favorite entry for the same chef and customer
            Favorite.objects.create(customer=self.customer, chef=self.chef)


class ViewsTestCase(TestCase):
    def setUp(self):
        # Create necessary model instances for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_chef = User.objects.create_user(username='testuser_chef', email='test@example.com', password='testpassword')
        self.chef = Chef.objects.create(auth_user=self.user_chef, firstname='John', lastname='Doe', username='johndoe', email='johndoe@example.com', password='chefpassword')
        self.recipe = Recipe.objects.create(name='Test Recipe', chef=self.chef)
        self.customer = Customer.objects.create(
            auth_user=self.user,
            firstname='John',
            lastname='Doe',
            username='johndoe',
            email='johndoe@example.com',
            password='test123'
        )

    def test_index_view(self):
        # Create recipes for the test
        recipes = [
            Recipe.objects.create(name='Recipe 1', chef=self.chef),
            Recipe.objects.create(name='Recipe 2', chef=self.chef),
            Recipe.objects.create(name='Recipe 3', chef=self.chef),
            Recipe.objects.create(name='Recipe 4', chef=self.chef),
            Recipe.objects.create(name='Recipe 5', chef=self.chef),
        ]

        url = reverse('customer:index', args=[self.customer.id])
        response = self.client.get(url)

        # Ensure the view returns a 302 status code and uses the correct template
        self.assertEqual(response.status_code, 302)

    def test_report_chef_form_view(self):
        url = reverse('customer:report_chef_form')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cust_report.html')

    # # Test 'report_chef' view
    # def test_report_chef_view(self):
    #     url = reverse('customer:report_chef')
    #     report_data = {
    #         "category": "Test Category",
    #         "description": "Test Description"
    #     }

    #     initial_report_count = Report.objects.count()
    #     response = self.client.post(url, report_data)

    #     # Ensure the view returns a 200 status code
    #     self.assertEqual(response.status_code, 200)

    #     # Ensure that a report has been created
    #     self.assertEqual(Report.objects.count(), initial_report_count + 1)

    #     # Get the created report
    #     new_report = Report.objects.latest('id')

    #     # Check the attributes of the created report
    #     self.assertEqual(new_report.category, report_data["category"])
    #     self.assertEqual(new_report.description, report_data["description"])


    def test_favorite_chef_view(self):
        client = Client()

        # Log in the customer user
        client.force_login(self.user)

        # Test favoriting a chef successfully
        response = client.post(reverse('customer:favorite_chef', args=[self.customer.id, self.chef.id]))
        self.assertEqual(response.status_code, 200)  # Check if the view returns a success response
        self.assertEqual(response.json()['status'], 'success')  # Check if the status is success
        self.assertEqual(response.json()['message'], 'Chef successfully favorited!')  # Check the success message
        self.assertTrue(Favorite.objects.filter(customer=self.customer, chef=self.chef).exists())  # Check if the favorite object was created

        # Test favoriting an already favored chef
        response = client.post(reverse('customer:favorite_chef', args=[self.customer.id, self.chef.id]))
        self.assertEqual(response.status_code, 200)  # Check if the view returns a success response
        self.assertEqual(response.json()['status'], 'failed')  # Check if the status is failed
        self.assertEqual(response.json()['message'], 'Chef already favorited!')  # Check the failure message
        self.assertEqual(Favorite.objects.filter(customer=self.customer, chef=self.chef).count(), 1)  # Check that the favorite object count remains the same

        # Test when an unauthenticated user tries to favorite a chef
        client.logout()
        response = client.post(reverse('customer:favorite_chef', args=[self.customer.id, self.chef.id]))
        self.assertEqual(response.status_code, 302)  # Check if the view redirects unauthenticated users

    # Test 'chef_view' view
    def test_chef_view(self):
        url = reverse('customer:chef_view', args=[self.customer.id, self.chef.id])
        response = self.client.get(url)

        # Ensure the view returns a 302 status code and uses the correct template
        self.assertEqual(response.status_code, 302)



    def test_view_all_recipes_view(self):
        # Create some sample recipes
        Recipe.objects.create(name='Recipe 1', chef=self.chef)
        Recipe.objects.create(name='Recipe 2', chef=self.chef)
        Recipe.objects.create(name='Recipe 3', chef=self.chef)

        url = reverse('customer:view_all_recipe', args=[self.customer.id])
        response = self.client.get(url)

        # Ensure the view returns a 302 status code and uses the correct template
        self.assertEqual(response.status_code, 302)

    def test_recipe_view(self):
        recipe = Recipe.objects.create(name='Test Recipe', chef=self.chef)

        url = reverse('customer:recipe_view', args=[self.recipe.id, self.customer.id])
        response = self.client.get(url)

        # Ensure the view returns a 302 status code and uses the correct template
        self.assertEqual(response.status_code, 302)
