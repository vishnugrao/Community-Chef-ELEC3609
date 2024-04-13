from django.urls import include, path
from . import views

app_name = 'profile_manager'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('logout/', views.user_logout, name="logout"),
    path('incorrect_user/', views.incorrect_user, name="incorrect_user"),
]