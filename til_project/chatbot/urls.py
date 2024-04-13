from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_ingredient, name='add_ingredient'),
    path('recipe', views.get_recipe, name= "get_recipe"),
    path('clear', views.clear_ingredients, name = "clear_ingredients"),
    path('delete_item', views.delete_item, name = "delete_item"),
]
