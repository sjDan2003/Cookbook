from sys import path
import urllib.request
from os.path import basename

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

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

class RecipeDetailView(DetailView):
    """Class based view to display
    """
    model = Recipe
    template_name = 'RecipeViewer/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(CreateView):
    model = Recipe
    fields = ['name', 'ingredients', 'instructions', 'image']
    template_name = 'RecipeViewer/recipe_create.html'

class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = ['name', 'ingredients', 'instructions', 'image']
    template_name = 'RecipeViewer/recipe_update.html'

class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'RecipeViewer/recipe_delete.html'
    context_object_name = 'recipe'
    success_url = '/'

def new_recipe_view(request):

    if request.method == 'POST':
        form = NewRecipeForm(request.POST)
        if form.is_valid():
            data, status_code = RecipeScraper().scrape_recipe_data(form.cleaned_data['recipe_url'])
            print(status_code)
            if status_code == 200:
                new_recipe = Recipe()
                # print(data['name'])
                # print(data['recipeIngredient'])
                # print(data['recipeInstructions'])
                # print(data['image'])
                new_recipe.name = data['name']
                new_recipe.ingredients = data['recipeIngredient']
                new_recipe.instructions = data['recipeInstructions']

                if data['image'] is not '':

                    print(data['image'])

                    request_headers = {}
                    request_headers['User-Agent'] = 'Mozilla/5.0'
                    status_code = 0

                    # Create a request so headers can be added
                    req = urllib.request.Request(data['image'], headers=request_headers)
                    try:
                        with urllib.request.urlopen(req) as response:
                            img_temp = NamedTemporaryFile(delete = True)
                            img_temp.write(response.read())
                            img_temp.flush()

                            new_recipe.image.save('image_{}'.format(basename(data['image'])), File(img_temp))

                    except urllib.error.HTTPError as http_error:

                        # Save the error code for this object.
                        # The GUI will later poll this code and output
                        # relevant information to the user.
                        status_code = http_error.code

                    except urllib.error.URLError as url_error:
                        # TODO: Investigate what URLErrors could happen
                        # and properly handle each one.
                        # For now just print the cause so the app doesn't crash
                        # on the user.
                        print(url_error.reason)



                new_recipe.save()
                # print(new_recipe.pk)
            return HttpResponseRedirect(reverse('index'))

    else:
        form = NewRecipeForm()

    return render(request, 'RecipeViewer/NewRecipe.html', {'form': form})
