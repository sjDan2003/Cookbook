from sys import path

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewRecipeForm
from .models import Recipe
path.append('..')
from RecipeScrapers import RecipeScraper

class RecipeListView(ListView):
    model = Recipe
    template_name = 'RecipeViewer/home.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'RecipeViewer/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(CreateView):
    model = Recipe
    fields = ['name', 'ingredients', 'instructions']
    template_name = 'RecipeViewer/recipe_create.html'

class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = ['name', 'ingredients', 'instructions']
    template_name = 'RecipeViewer/recipe_create.html'

def NewRecipeView(request):

    if request.method == 'POST':
        form = NewRecipeForm(request.POST)
        if form.is_valid():
            data, status_code = RecipeScraper().scrape_recipe_data(form.cleaned_data['recipe_url'])
            print(status_code)
            if status_code == 200:
                # new_recipe = Recipe()
                # new_recipe.name = data['name']
                # new_recipe.ingredients = '\n'.join(data['recipeIngredient'])
                print(data['name'])
                print(data['recipeIngredient'])
                print(data['recipeInstructions'])
                # print(data['image'])
                # new_recipe.name = data['name']
                # new_recipe.ingredients = data['recipeIngredient']
                # new_recipe.instructions = data['recipeInstructions']
                # new_recipe.save()
                # print(new_recipe.pk)
            return HttpResponseRedirect(reverse('index'))

    else:
        form = NewRecipeForm()

    return render(request, 'RecipeViewer/NewRecipe.html', {'form': form})
