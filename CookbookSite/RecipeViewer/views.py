from sys import path
import urllib.request
from os.path import basename

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Q

from .forms import NewRecipeForm
from .models import Recipe
path.append('..')
from RecipeScrapers import RecipeScraper

class RecipeListView(ListView):
    """Class based view to manage viewing all the
       recipes on a single page
    """

    model = Recipe
    template_name = 'RecipeViewer/home.html'
    context_object_name = 'recipes'

class RecipeSearchView(ListView):
    """Class based view to manage viewing all the
       recipes on a single page
    """

    model = Recipe
    template_name = 'RecipeViewer/recipe_search.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        query = self.request.GET.get('search_input')
        recipe_list = Recipe.objects.filter(
            Q(name__icontains=query) | Q(ingredients__icontains=query)
        )
        return recipe_list

class RecipeDetailView(DetailView):
    """Class based view to display
    """
    model = Recipe
    template_name = 'RecipeViewer/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(CreateView):
    """Class based view to create a new recipe from manually
       entering the details
    """
    model = Recipe
    fields = ['name', 'ingredients', 'instructions', 'image']
    template_name = 'RecipeViewer/recipe_create.html'

class RecipeUpdateView(UpdateView):
    """Class based view to update an existing recipe
    """
    model = Recipe
    fields = ['name', 'ingredients', 'instructions', 'image']
    template_name = 'RecipeViewer/recipe_update.html'

class RecipeDeleteView(DeleteView):
    """Class based view to delete an existing recipe
    """
    model = Recipe
    template_name = 'RecipeViewer/recipe_delete.html'
    context_object_name = 'recipe'
    success_url = '/'

def new_recipe_view(request):
    """Function based view to handle importing a recipe from a URL.
       This function will call the RecipeScraper function to scrape the data
       and use the dictionary that is returned to create a new recipe object.
       If there is an image then it will be downloaded and saved to the media folder

       Args:
            request: Beautiful Soup object containing the recipe data

        Returns:
            A dictionary containing all of the relevant recipe data
    """

    if request.method == 'POST':
        form = NewRecipeForm(request.POST)
        if form.is_valid():
            data, status_code = RecipeScraper().scrape_recipe_data(form.cleaned_data['recipe_url'])
            if status_code == 200:

                new_recipe = Recipe()
                new_recipe.name = data['name']
                new_recipe.ingredients = data['recipeIngredient']
                new_recipe.instructions = data['recipeInstructions']
                new_recipe.url = form.cleaned_data['recipe_url']

                if data['image'] is not '':

                    img_data, status_code = RecipeScraper().get_html_data(data['image'])
                    img_temp = NamedTemporaryFile(delete = True)
                    img_temp.write(img_data)
                    img_temp.flush()

                    new_recipe.image.save('image_{}'.format(basename(data['image'])),
                                            File(img_temp))

                new_recipe.save()
                # print(new_recipe.pk)
            return HttpResponseRedirect(reverse('index'))

    else:
        form = NewRecipeForm()

    return render(request, 'RecipeViewer/NewRecipe.html', {'form': form})
