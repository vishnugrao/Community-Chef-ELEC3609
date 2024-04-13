from django.test import TestCase, Client
from django.db import IntegrityError
from .models import CaseInsensitiveCharField, Ingredient
from django.http import HttpResponseRedirect, JsonResponse
from .forms import IngredientForm
from django.urls import reverse

class CaseInsensitiveCharFieldTest(TestCase):

    def test_prep_value(self):
        """Test that the CaseInsensitiveCharField preps values correctly."""

        field = CaseInsensitiveCharField()

        # Test that values are converted to lowercase.
        self.assertEqual(field.get_prep_value("FOO"), "Foo")
        self.assertEqual(field.get_prep_value("bAr"), "Bar")

        # Test that values are capitalized.
        self.assertEqual(field.get_prep_value("foo"), "Foo")
        self.assertEqual(field.get_prep_value("bar"), "Bar")

        # Test that None values are returned unchanged.
        self.assertEqual(field.get_prep_value(None), None)

class IngredientTest(TestCase):

    def test_create_ingredient(self):
        """Test that an ingredient can be created successfully."""

        # Create a new ingredient object.
        ingredient = Ingredient(name="Salt")

        # Save the ingredient to the database.
        ingredient.save()

        # Get the ingredient from the database.
        saved_ingredient = Ingredient.objects.get(pk=ingredient.pk)

        # Assert that the two ingredient objects are equal.
        self.assertEqual(ingredient, saved_ingredient)

    def test_unique_name_constraint(self):
        """Test that the unique name constraint is enforced."""

        # Create an ingredient object.
        ingredient = Ingredient(name="Salt")
        ingredient.save()

        # Try to create another ingredient object with the same name.
        another_ingredient = Ingredient(name="Salt")

        with self.assertRaises(IntegrityError):
            another_ingredient.save()

    def test_str_method(self):
        """Test that the str() method returns the correct string representation of an ingredient object."""

        ingredient = Ingredient(name="Salt")

        # Assert that the str() method returns the ingredient's name.
        self.assertEqual(str(ingredient), ingredient.name)

class AddIngredientViewTest(TestCase):

    def test_get(self):
        """Test that the add_ingredient view returns a 200 OK response."""

        client = Client()
        response = client.get(reverse("add_ingredient"))

        self.assertEqual(response.status_code, 200)

    def test_post_valid_form(self):
        """Test that the add_ingredient view saves a new ingredient object when a valid form is submitted."""

        client = Client()
        data = {"name": "Salt"}
        response = client.post(reverse("add_ingredient"), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_post_invalid_form(self):
        """Test that the add_ingredient view adds nothing when an invalid form is submitted."""

        client = Client()
        data = {"name": ""}
        response = client.post(reverse("add_ingredient"), data=data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredient.objects.count(), 0)

class DeleteItemViewTest(TestCase):

    def test_post(self):
        """Test that the delete_item view deletes an ingredient object when a valid POST request is made."""

        client = Client()

        # Create an ingredient object
        ingredient = Ingredient.objects.create(name="Salt")

        # Delete the ingredient object
        response = client.post(reverse("delete_item"), data={"item_id": ingredient.pk})

        # Assert that the ingredient object is deleted
        self.assertEqual(Ingredient.objects.count(), 0)

class ClearIngredientsViewTest(TestCase):

    def test_get(self):
        """Test that the clear_ingredients view deletes all ingredient objects when a GET request is made."""

        client = Client()

        # Create a few ingredient objects
        Ingredient.objects.create(name="Salt")
        Ingredient.objects.create(name="Pepper")

        # Delete all ingredient objects
        response = client.get(reverse("clear_ingredients"))

        # Assert that all ingredient objects are deleted
        self.assertEqual(Ingredient.objects.count(), 0)

class GetRecipeViewTest(TestCase):

    def test_get(self):
        """Test that the get_recipe view returns a 200 OK response."""

        client = Client()
        response = client.get(reverse("get_recipe"))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Test that the get_recipe view returns a recipe suggestion when a POST request is made with a list of ingredients."""

        client = Client()
        data = {"ingredients": ["Salt", "Pepper"]}
        response = client.post(reverse("get_recipe"), data=data)

        # Assert that the response is a text file
        self.assertEqual(response.get("content-type"), "text/html; charset=utf-8")
