from django.db import models
from chef.models import Recipe, Chef

from django.contrib.auth.models import User

class Customer(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)

    firstname = models.CharField(max_length=225)
    lastname = models.CharField(max_length=225)
    username = models.CharField(max_length=225,unique=True)
    email = models.EmailField(max_length=225)
    password = models.CharField(max_length=225)
    # image = models.ImageField(upload_to='images/', default='/images/default_chef.png')


class Clap(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # To keep track of when the clap was given

    class Meta:
        unique_together = (('customer', 'recipe'),)  # Ensuring a customer can clap only once for a particular recipe

    def __str__(self):
        return f"{self.customer.username} clapped for {self.recipe.name}"

class Favorite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # To keep track of when the chef was added to favorites

    class Meta:
        unique_together = (('customer', 'chef'),)  # Ensuring a customer can add a chef to favorites only once

    def str(self):
        return f"{self.customer.username} favorited chef {self.chef.username}"