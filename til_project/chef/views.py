from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .create_chef_form import ChefRegistrationForm
from .create_chef_form import RecipeRegistrationForm
from .login_form import LoginForms
from .AvailabilityForm import AvailabilityForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Availability, Recipe, Chef, Ingredient
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
import json
from django.forms.models import model_to_dict

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from utilities.models import Report

from chat.models import ChatRoom

from .models import Recipe, Chef, Availability, Recipe, Chef, Ingredient
from .models import Availability, Recipe, Chef, Ingredient

from .create_chef_form import ChefRegistrationForm, RecipeRegistrationForm
from .login_form import LoginForms

LOGIN_URL = '/chef/chef_login/'

def chef_login(request):
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = authenticate(request, username=username, password=password)

                if user is None:
                    print(user)
                    messages.error(request, 'invalid username or password. Please try again')
                    return render(request, 'chef_login.html', {'form': form, 'invalid': True})

                login(request, user)
                chef_user = Chef.objects.get(username=username)

                messages.success(request, f'Hello {chef_user.username}! You have been logged in')
                return redirect(reverse('chef:chef_home', args=[chef_user.id]))

            except Chef.DoesNotExist:
                messages.error(request, 'YOU AINT EVEN A USER BRO')
                return render(request, 'chef_login.html', {'form': form, 'invalid': True})
    else:
        form = LoginForms()
    
    return render(request, 'chef_login.html', {'form': form})



def create_chef_profile(request):
    # template = loader.get_template('create_chef_profile.html')
    if request.method == 'POST':
        form = ChefRegistrationForm(request.POST)
        if form.is_valid():
            chef = form.save(commit=False)

            new_user = User(username=chef.username, email=chef.email)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            chef.auth_user = new_user
            chef.save()

            print("You have sucessfully created an account")

            login(request, chef.auth_user)
            return redirect(reverse('chef:chef_home', args=[chef.id]))
    else:
        form = ChefRegistrationForm()

    return render(request, 'create_chef_profile.html', {'form': form})
    # return HttpResponse(template.render(None, request))


@login_required(login_url=LOGIN_URL)
def chef_home(request, id):
    user_db = Chef.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
        
    print(request.user.id)
    print(request.user.is_authenticated)
    try:
        user = Chef.objects.get(id=id)
        recipes = Recipe.objects.filter(chef=user)

        chef_name = user.username.capitalize()
    except Chef.DoesNotExist:
        chef_name = "Guest"  # Provide a default value if the user doesn't exist or if there's an error

    context = {'chef_name': chef_name, 'id': id, 'chef': user, 'recipes': recipes}
    return render(request, 'chef_home.html', context)


@login_required(login_url=LOGIN_URL)
def add_recipe(request, id):
    user_db = Chef.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
        
    if request.method == "POST":
        form = RecipeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new recipe
            recipe = form.save(commit=False)
            recipe.chef = Chef.objects.get(id=id)  # Assuming you have user authentication
            recipe.save()

            # Process ingredients
            ingredient_names = request.POST.getlist("ingredient_name")
            ingredient_prices = request.POST.getlist("ingredient_price")
            total_price = 0
            for name, price in zip(ingredient_names, ingredient_prices):
                # Create a new ingredient and associate it with the recipe
                if name and price:
                    ingredient = Ingredient.objects.create(name=name, price=price)
                    recipe.ingredients.add(ingredient)
                    total_price += float(price)
                    
                
            recipe.total_price = total_price + 0.20 * total_price #15% surcharge
            print(recipe.total_price)
            recipe.save()
            form = RecipeRegistrationForm()  # Redirect to a recipe list view
    else:
        form = RecipeRegistrationForm()

    return render(request, "chef_recipe.html", {"form": form, "id": id})


@login_required(login_url=LOGIN_URL)
def chef_profile(request, id):
    user_db = Chef.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    try:
        user = Chef.objects.get(id=id)
        recipes = Recipe.objects.filter(chef=user)
    except Chef.DoesNotExist:
        # Handle the case where the user doesn't exist
        # You can redirect or display an error message
        pass

    context = {'chef': user, 'recipes': recipes}
    return render(request, 'chef_profile.html', context)


@login_required(login_url=LOGIN_URL)
def display_recipes(request, id):
    user_db = Chef.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
        
    try:
        user = Chef.objects.get(id=id)
        recipes = Recipe.objects.filter(chef=user)
    except Chef.DoesNotExist:
        # Handle the case where the user doesn't exist
        # You can redirect or display an error message
        pass
    
    context = {'chef': user, 'recipes': recipes.reverse()}
    return render(request, 'all_recipe.html', context)


def recipe_profile(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    chef = recipe.chef
    total_price = sum(ingredient.price for ingredient in recipe.ingredients.all())
    context = {'recipe': recipe, 'chef':chef, 'total_price': total_price}
    return render(request, 'recipe_profile.html', context)


@login_required(login_url=LOGIN_URL)
def update_profile(request, id):
    user_db = Chef.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
        
    try:
        user = Chef.objects.get(id=id)
    except Chef.DoesNotExist:
        # Handle the case where the user doesn't exist
        # You can redirect or display an error message
        pass

    if request.method == 'POST':
        # Process the form data to update the user's profile
        # You can add the form handling logic here
        # After successfully updating the profile, you can redirect back to the profile page
        user.username = request.POST['username']
        user.firstname = request.POST['firstname']
        user.lastname = request.POST['lastname']
        user.email = request.POST['email']
        user.password = request.POST['password']
        
        # Check if a new image was uploaded
        if 'image' in request.FILES:
            user.image = request.FILES['image']

        # Save the updated user object
        user.save()

        return redirect(reverse('chef:chef_profile', args=[user.id]))

    context = {'user': user}
    return render(request, 'update_profile.html', context)


@login_required(login_url=LOGIN_URL)
def chef_availability(request, id):
    user_db = Chef.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
        
    chef = get_object_or_404(Chef, id=id)  # Use get_object_or_404 to handle invalid chef IDs
    availabilities = Availability.objects.filter(chef=chef)

def chef_availability(request, id):
    chef = get_object_or_404(Chef, id=id)
    availabilities = Availability.objects.filter(chef=chef)

    events = []
    for availability in availabilities:
        event = {
            'title': f'Availability - {availability.additional_info}',
            'start': str(availability.date) + 'T' + str(availability.start_time),
            'end': str(availability.date) + 'T' + str(availability.end_time),
            'id': availability.id,
        }

        events.append(event)

    events_json = json.dumps(events)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability_data = {
                'date': request.POST['date'],
                'start_time': request.POST['start_time'],
                'end_time': request.POST['end_time'],
                'vacancies': int(request.POST['vacancies']),
                'filled_seats': int(request.POST['filled_seats']),
                'additional_info': request.POST['additional_info'],
            }

            if availability_data['start_time'] >= availability_data['end_time']:
                raise ValidationError("Start time must be before end time")

            if availability_data['vacancies'] < 0:
                raise ValidationError("Vacancies cannot be negative")

            if availability_data['filled_seats'] < 0:
                raise ValidationError("Filled seats cannot be negative")

            if availability_data['filled_seats'] > availability_data['vacancies']:
                raise ValidationError("Filled seats cannot exceed vacancies")

            existing_overlapping_availability = Availability.objects.filter(
                chef=chef,
                date=availability_data['date'],
                start_time__lt=availability_data['end_time'],
                end_time__gt=availability_data['start_time']
            ).first()

            if existing_overlapping_availability:
                raise ValidationError("Availability overlaps with an existing booking")

            max_vacancies = 100

            if availability_data['vacancies'] > max_vacancies:
                raise ValidationError("Vacancies exceed the maximum limit")

            existing_availability = Availability.objects.filter(
                chef=chef,
                date=availability_data['date'],
                start_time=availability_data['start_time'],
                end_time=availability_data['end_time']
            ).first()

            if not existing_availability:
                availability = form.save(commit=False)
                availability.chef = chef
                availability.save()
                form = AvailabilityForm()
    else:
        form = AvailabilityForm()

    return render(request, 'availabilities.html', {"chef": chef, "events": events_json})

def get_chef_availabilities(request, id):
    chef = get_object_or_404(Chef, id=id)
    availabilities = Availability.objects.filter(chef=chef)

    events = []

    for availability in availabilities:
        event = {
            'title': f'Availability - {availability.additional_info}',
            'start': str(availability.date) + 'T' + str(availability.start_time),
            'end': str(availability.date) + 'T' + str(availability.end_time),
            'id': availability.id,  # Include the availability ID if needed
        }
        events.append(event)

    return JsonResponse(events, safe=False)


@login_required(login_url=LOGIN_URL)
def report_customer_form(request):
    return render(request, 'report_customer_form.html')


@login_required(login_url=LOGIN_URL)
def report_customer(request):
    if request.method == 'POST':
        category = request.POST['category']
        description = request.POST['description']

        new_report = Report(category=category, description=description)
        new_report.save()

        return HttpResponse("Your report has been submitted.")
    

@login_required(login_url=LOGIN_URL)
def chef_chats(request, id):
    user_db = Chef.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    chef = Chef.objects.get(id = id)

    rooms = ChatRoom.objects.filter(chef_id=chef)
    print(rooms)
    return render(request, 'chef_chats.html', {'id': id, 'rooms': rooms})
