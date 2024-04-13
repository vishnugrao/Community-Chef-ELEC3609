from django.db import models
from django.contrib.auth.models import User

class Availability(models.Model):
    date = models.DateField()
    vacancies = models.IntegerField()
    filled_seats = models.IntegerField()

class Chef(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    firstname = models.CharField(max_length=225)
    lastname = models.CharField(max_length=225)
    username = models.CharField(max_length=225,unique=True)
    email = models.EmailField(max_length=225)
    password = models.CharField(max_length=225)
    image = models.ImageField(upload_to='images/', default='/images/default_chef.png')
    # availabilities = models.ManyToManyField(Availability, default=None)
    
class Availability(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    vacancies = models.IntegerField()
    filled_seats = models.IntegerField()
    additional_info = models.TextField()

class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    price = models.DecimalField(default=-1, decimal_places=2, max_digits=6)

class Recipe(models.Model):
    # ID created by default https://docs.djangoproject.com/en/4.2/topics/db/models/
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=256)
    description = models.TextField()
    claps = models.PositiveIntegerField(default = 0)
    #add ingredients and price
    image = models.ImageField(upload_to='images/', default='/images/default_rec.png')
    total_price = models.DecimalField(default=-1, decimal_places=2, max_digits=6)
    ingredients = models.ManyToManyField(Ingredient)
