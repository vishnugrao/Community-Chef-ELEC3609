from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Ingredient
from .forms import IngredientForm
from django.conf import settings
from django.urls import reverse
import openai
from django.http import JsonResponse

prompt_template = """Suggest me a recipe with the following ingredients:
{}
Also in the following format:
"Title: 
Ingredients:
Instructions:
"""

def add_ingredient(request):
    # logic of view will be implemented here
    error_message = ""
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error_message = "An item with this value already exists."
            form.add_error('name', 'This element already exists.')
    else:
        form = IngredientForm()  
    ingredients = Ingredient.objects.all()
    return render(request, "add_ingredient.html", {'form': form, 'ingredients': ingredients, 'error_message': error_message})

def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        # Delete the item from the database
        # You'll need to add your actual item deletion logic here
        Ingredient.objects.get(id=item_id).delete()

        return redirect(reverse("add_ingredient"))

    return JsonResponse({'message': 'Invalid request'}, status=400)

def clear_ingredients(request):
    Ingredient.objects.all().delete()
    return redirect(reverse("add_ingredient"))

# HTTP Request to get a recipe recipe
def get_recipe(request):
    ingredients = Ingredient.objects.all()
    ingredient_list = ", ".join([i.name for i in ingredients])

    # Use ChatGPT API to get recipe suggestion
    recipe = get_recipe_suggestion(ingredient_list)

    title, ingredients, instructions = parse_recipe_text(recipe)

    return render(request, 'display.html', {'recipe': recipe, 'title': title, 'ingredients': ingredients, 'instructions': instructions})

# ChatGPT API to get recipe suggestion
def get_recipe_suggestion(ingredient_list):

    # Access your OpenAI API key from settings
    api_key = getattr(settings, "OPENAI_API_KEY", None)

    
    # Set the OpenAI API key
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": prompt_template.format(ingredient_list)
            }
        ],
        max_tokens=500
    )

    Ingredient.objects.all().delete()
    
    return response['choices'][0]['message']['content']

# Test function to get recipe suggestion
def get_recipe_suggestion_test(ingredient_list):
    response = """Title: Peppered Scrambled Eggs

Ingredients:
- 4 large eggs
- 1/4 teaspoon black pepper
- Salt to taste
- 1 tablespoon butter
- 2 tablespoons milk (optional)

Instructions:
1. Crack the eggs into a bowl and beat them until the yolks and whites are fully combined. Season with 1/4 teaspoon of black pepper and a pinch of salt, adjusting the salt to your taste.

2. In a non-stick skillet, melt 1 tablespoon of butter over medium heat. You can add a bit more for extra richness if you like.

3. Pour the beaten eggs into the skillet. For extra creamy eggs, add 2 tablespoons of milk at this point and stir gently.

4. Continuously stir the eggs as they cook, pushing them from the edges towards the center. This will create soft, fluffy curds.

5. Cook until the eggs are just set but still slightly creamy. Avoid overcooking, as eggs can become dry.

6. Serve immediately, garnished with a sprinkle of black pepper for extra flavor.

Enjoy your delicious Peppered Scrambled Eggs!
"""
    Ingredient.objects.all().delete()
    return response

def parse_recipe_text(recipe_text):
    title = None
    ingredients = None
    instructions = None

    lines = recipe_text.split('\n')

    current_section = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("Title:"):
            current_section = "title"
            title = line[len("Title: "):].strip()
        elif line.startswith("Ingredients:"):
            current_section = "ingredients"
            ingredients = []
        elif line.startswith("Instructions:"):
            current_section = "instructions"
            instructions = []
        else:
            if current_section == "ingredients":
                ingredients.append(line.strip("- "))
            elif current_section == "instructions":
                instructions.append(line)

    # Join the ingredients and instructions lists into strings
    # ingredients = "\n".join(ingredients) if ingredients else None
    # instructions = "\n".join(instructions) if instructions else None

    return title, ingredients, instructions
