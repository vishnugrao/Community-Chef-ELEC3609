from django.urls import path
from . import views

app_name = 'chef'

urlpatterns = [
    path('chef_login/', views.chef_login, name="chef_login"),
    path('create-chef-profile/', views.create_chef_profile, name="create_chef_profile"),
    path('chef_home/<int:id>/', views.chef_home, name="chef_home"),
    path('chef_profile/<int:id>/', views.chef_profile, name='chef_profile'),
    path('update_profile/<int:id>/', views.update_profile, name='update_profile'),
    path('availability/<int:id>/', views.chef_availability, name='chef_availability'),
    # path('book/<int:id>/', views.book_availability, name='book_availability'),
    # path('events/<int:id>/', views.availability_events, name='availability_events'),
    path('add_recipe/<int:id>/', views.add_recipe, name='add_recipe'),
    path('display_recipes/<int:id>/', views.display_recipes, name='display_recipes'),
    path('report_customer_form/', views.report_customer_form, name='report_customer_form'),
    path('report_customer/', views.report_customer, name='report_customer'),
    path('recipe/<int:recipe_id>/', views.recipe_profile, name='recipe_profile'),
    path('get_chef_availabilities/<int:id>/', views.get_chef_availabilities, name='get_chef_availabilities'),
    path('chef_chats/<int:id>/', views.chef_chats, name='chef_chats'),
]

