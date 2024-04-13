from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path("index/<int:id>/", views.index, name="index"),
    path("report_chef_form/", views.report_chef_form, name="report_chef_form"),
    path("report_chef/", views.report_chef, name="report_chef"),
    path('customer_login/', views.customer_login, name="customer_login"),
    path('create_customer_profile/', views.create_customer_profile, name="create_customer_profile"),
    path('claps/<int:id>', views.clapped, name = 'claps'),
    path('claps/<int:user_id>/<int:recipe_id>/', views.clapped, name='claps'),
    path('liked_chefs/<int:user_id>/', views.liked_chefs, name='liked_chefs'),
    path('favorite_chef/<int:user_id>/<int:chef_id>', views.favorite_chef, name='favorite_chef'),
    path('view-all-recipe/<int:id>', views.view_all_recipes, name= 'view_all_recipe'),
    path('recipe/<int:recipe_id>/<int:customer_id>', views.recipe_view, name='recipe_view'),
    path('chef/<int:customer_id>/<int:chef_id>', views.chef_view, name='chef_view'),

]