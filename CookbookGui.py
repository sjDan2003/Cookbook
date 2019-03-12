from kivy.app import App
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from WebsiteScraper import RecipeObjectClass


class RecipeButton(ListItemButton):
    pass


class CookbookLayout(GridLayout):
    recipeList = ObjectProperty()
    recipeName = ObjectProperty()
    recipeInstructions = ObjectProperty()
    recipeIngredients = ObjectProperty()

    def ChangeRecipe(self, newRecipe):

        url = 'https://www.runnersworld.com/recipes/irish-pork-stew-with-irish-stout-and-caraway-seeds'

        recipeObj = RecipeObjectClass(url)
        if recipeObj.validData:
            self.recipeName.text = recipeObj.GetRecipeName()
            self.recipeInstructions.text = recipeObj.GetInstructions()
            self.recipeIngredients.text = ''
            for ingredient in recipeObj.GetIngredients():
                self.recipeIngredients.text += '\n{}'.format(ingredient)

            if len(self.recipeName.text) > 20:
                self.recipeName.font_size = "25dp"


class CookbookGuiApp(App):
    def build(self):
        return CookbookLayout()
