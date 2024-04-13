from django.contrib import admin
from .models import Recipe, Ingredient, Chef, Availability

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Chef)
admin.site.register(Ingredient)
admin.site.register(Availability)