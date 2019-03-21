from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from WebsiteScraper import RecipeObjectClass


class RecipeButton(Button):

    def ChangeRecipe(self, recipeData):
        app = App.get_running_app()
        app.root.get_screen('recipe view').recipeName.text = recipeData.GetRecipeName()
        app.root.get_screen('recipe view').recipeInstructions.text = recipeData.GetInstructions()
        app.root.get_screen('recipe view').recipeName.text = recipeData.GetRecipeName()
        app.root.get_screen('recipe view').recipeIngredients.text = ''
        for ingredient in recipeData.GetIngredients():
            app.root.get_screen('recipe view').recipeIngredients.text += '\n{}'.format(ingredient)


class RecipeImportScreen(Screen):

    urlInput = ObjectProperty()
    recipeName = ObjectProperty()
    recipeInstructions = ObjectProperty()
    recipeIngredients = ObjectProperty()
    recipeObj = RecipeObjectClass()

    def ImportRecipe(self):

        url = 'https://www.runnersworld.com/recipes/irish-pork-stew-with-irish-stout-and-caraway-seeds'

        self.recipeObj.GetRecipeFromUrl(self.urlInput.text)
        #self.recipeObj.GetRecipeFromUrl(url)
        if self.recipeObj.validData:
            self.recipeName.text = self.recipeObj.GetRecipeName()
            self.recipeInstructions.text = self.recipeObj.GetInstructions()
            self.recipeIngredients.text = ''
            for ingredient in self.recipeObj.GetIngredients():
                self.recipeIngredients.text += '\n{}'.format(ingredient)

            if len(self.recipeName.text) > 20:
                self.recipeName.font_size = "25dp"

    def CancelRecipeImport(self):
        self.urlInput.text = ''
        self.recipeName.text = ''
        self.recipeInstructions.text = ''
        self.recipeIngredients.text = ''
        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'

    def ConfirmRecipeImport(self):

        # Update the ListView to include the new recipe
        newRecipeObj = RecipeObjectClass(self.recipeObj)
        self.manager.get_screen('recipe view').recipeList.data.append({"color": (1, 1, 1, 1), "font_size": "10sp", "text": newRecipeObj.GetRecipeName(), "input_data": newRecipeObj})
        print(self.manager.get_screen('recipe view').recipeList.data)
        # Update the current view with the new recipe
        self.manager.get_screen('recipe view').recipeName.text = self.recipeObj.GetRecipeName()
        self.manager.get_screen('recipe view').recipeDict[self.recipeObj.GetRecipeName()] = self.recipeObj

        # Transition back to the recipe view screen
        self.manager.transition.direction = 'right'
        self.manager.current = 'recipe view'


class RecipeViewScreen(Screen):
    recipeList = ObjectProperty()
    recipeName = ObjectProperty()
    recipeInstructapions = ObjectProperty()
    recipeIngredients = ObjectProperty()
    recipeDict = {}

    def ChangeRecipe(self, newRecipe):

        print(newRecipe)
        recipeObj = self.recipeDict[newRecipe]
        print(recipeObj.data)
        if recipeObj.validData:
            self.recipeName.text = recipeObj.GetRecipeName()
            self.recipeInstructions.text = recipeObj.GetInstructions()
            self.recipeIngredients.text = ''
            for ingredient in recipeObj.GetIngredients():
                self.recipeIngredients.text += '\n{}'.format(ingredient)

            if len(self.recipeName.text) > 20:
                self.recipeName.font_size = "25dp"
        pass

    def ChangeRecipeName(self):

        print(self.recipeDict.keys())
        pass


class CookbookGuiApp(App):

    def build(self):
        cookbooxScreenManager = ScreenManager()
        cookbooxScreenManager.add_widget(RecipeViewScreen())
        cookbooxScreenManager.add_widget(RecipeImportScreen())
        return cookbooxScreenManager
