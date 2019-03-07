from kivy.app import App
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout

from WebsiteScraper import RecipeObjectClass


class RecipeButton(ListItemButton):
    pass


class CookbookLayout(GridLayout):
    recipeList = ObjectProperty()
    recipeName = ObjectProperty()
    recipeInstructions = ObjectProperty()
    recipeIngredients = ObjectProperty()

    def ChangeRecipe(self, newRecipe):
        #self.recipeName.text = newRecipe
        print('Here' + newRecipe)
        url = 'https://www.runnersworld.com/recipes/irish-pork-stew-with-irish-stout-and-caraway-seeds'

        recipeObj = RecipeObjectClass(url)
        if recipeObj.validData:
            print(recipeObj.GetIngredients())
            self.recipeName.text = recipeObj.GetRecipeName()
            self.recipeInstructions.text = recipeObj.GetInstructions()
            self.recipeIngredients.text = ''
            for ingredient in recipeObj.GetIngredients():
                self.recipeIngredients.text += '\n{}'.format(ingredient)


class CookbookGuiApp(App):
    def build(self):
        return CookbookLayout()
