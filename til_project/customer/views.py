from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .create_cust_form import CustomerRegistrationForm
from .login_form import CustomerLoginForms
from .models import Customer, Favorite, Clap

from chef.models import Recipe, Chef

from utilities.models import Report

LOGIN_URL = '/customer/customer_login/'

@login_required(login_url=LOGIN_URL)
def index(request, id):
    user_db = Customer.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    try:
        user = Customer.objects.get(id=id)
        recipes = Recipe.objects.all()
        if(len(recipes) > 5):
            top_five = recipes[len(recipes) - 5:]
        else:
            top_five = recipes.reverse()
    except Customer.DoesNotExist:
        cust_name = "Guest"  # Provide a default value if the user doesn't exist or if there's an error
    #print 5 most recent recipes
    context = {'user': user, 'id': id, 'recipes':top_five }
    return render(request, 'cust_home.html', context)


def report_chef_form(request):
    return render(request, "cust_report.html")


def report_chef(request):
    new_report = Report(category=request.POST["category"], description=request.POST["description"])
    new_report.save()

    return HttpResponse("Your report has been submitted.")


def create_customer_profile(request):
    # template = loader.get_template('create_chef_profile.html')
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)

            new_user = User(username=customer.username, email=customer.email)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            customer.auth_user = new_user
            customer.save()

            login(request, customer.auth_user)
            print("You have sucessfully created an account")
            return redirect(reverse('customer:index', args=[customer.id]))
    else:
        form = CustomerRegistrationForm()

    return render(request, 'create_profile.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        form = CustomerLoginForms(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            try:
                user = authenticate(request, username=username, password=password)

                if user is None:
                    print(user)
                    messages.error(request, 'invalid username or password. Please try again')
                    return render(request, 'cust_login.html', {'form': form, 'invalid': True})
                
                login(request, user)
                user = Customer.objects.get(username=username)

                messages.success(request, f'Hello {user.username}! You have been logged in')
                print("logged in")
                return redirect(reverse('customer:index', args=[user.id]))
        
            except Customer.DoesNotExist:
                messages.error(request, 'YOU AINT EVEN A USER BRO')
                return render(request, 'chef_login.html', {'form': form, 'invalid': True})
    else:
        form = CustomerLoginForms()
    
    return render(request, 'cust_login.html', {'form': form})


@login_required(login_url=LOGIN_URL)
def clapped(request,id):
    user_db = Customer.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    customer = Customer.objects.get(pk= id)
    claps = Clap.objects.filter(customer=customer) 
    recipes = [clap.recipe for clap in claps]
    
    context = {
        'clapped_recipes': recipes,
        'customer': customer
    }
    return render(request, 'clap.html', context)


@login_required(login_url=LOGIN_URL)
def clap_recipe(request, user_id, recipe_id):
    user_db = Customer.objects.get(id=user_id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    if request.method == "POST": 
        if not (user_id and recipe_id):
            return JsonResponse({'error': 'user_id and recipe_id are required'}, status=400)

        customer = get_object_or_404(Customer, id=user_id)
        recipe = get_object_or_404(Recipe, id=recipe_id)

        
        clap_exists = Clap.objects.filter(customer=customer, recipe=recipe).exists()
        if clap_exists:
            return JsonResponse({'message': 'Recipe already clapped by user'}, status=400)

        Clap.objects.create(customer=customer, recipe=recipe)

        return JsonResponse({'message': 'Recipe clapped successfully'})
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    

@login_required(login_url=LOGIN_URL)
def liked_chefs(request, user_id):
    user_db = Customer.objects.get(id=user_id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    user = get_object_or_404(Customer, id=user_id)
    favorites = Favorite.objects.filter(customer=user)
    chefs = [favorite.chef for favorite in favorites]
    return render(request, 'fav_chef.html', {'liked_chefs': chefs})


@login_required(login_url=LOGIN_URL)
def favorite_chef(request, user_id, chef_id):
    user_db = Customer.objects.get(id=user_id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    if request.method == 'POST':
        try:
            user = get_object_or_404(Customer, id=user_id)
            chef = get_object_or_404(Chef, id=chef_id)
            if not Favorite.objects.filter(customer=user, chef=chef).exists():
                Favorite.objects.create(customer=user, chef=chef)
                return JsonResponse({'status': 'success', 'message': 'Chef successfully favorited!'})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Chef already favorited!'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
        
#everything related to recipes, and the chef views are from here on 

@login_required(login_url=LOGIN_URL)
def chef_view(request, customer_id, chef_id):
    user_db = Customer.objects.get(id=customer_id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    try:
        user = Chef.objects.get(id=chef_id)
        recipes = Recipe.objects.filter(chef=user)
    except Chef.DoesNotExist:
        # Handle the case where the user doesn't exist
        # You can redirect or display an error message
        pass

    context = {'chef': user, 'recipes': recipes, 'customer_id': customer_id}
    return render(request, 'chef_view.html', context)


@login_required(login_url=LOGIN_URL)
def view_all_recipes(request, id):
    user_db = Customer.objects.get(id=id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    try:
        user = Customer.objects.get(id=id)
        recipes = Recipe.objects.all()
    except Chef.DoesNotExist:
        # Handle the case where the user doesn't exist
        # You can redirect or display an error message
        pass

    context = {'user': user, 'recipes': recipes, 'customer_id': id}
    return render(request, 'view_all_recipe.html', context)


@login_required(login_url=LOGIN_URL)
def recipe_view(request, recipe_id, customer_id):
    user_db = Customer.objects.get(id=customer_id)
    if request.user.is_authenticated and request.user.id != user_db.auth_user.id:
        return redirect(reverse("profile_manager:incorrect_user"))
    
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    chef = recipe.chef
    user = Customer.objects.get(id=customer_id)
    context = {'user': user, 'recipe': recipe, 'chef': chef, 'customer_id': customer_id,}
    return render(request, 'recipe_view.html', context)


